"""Data coordinator for Backup Guardian."""
import hashlib
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import hassio
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN, 
    UPDATE_INTERVAL,
    CONF_GOOGLE_DRIVE_ENABLED,
    CONF_GOOGLE_CLIENT_ID,
    CONF_GOOGLE_CLIENT_SECRET,
    CONF_GOOGLE_FOLDER_ID,
    CONF_GOOGLE_TOKEN,
)
from .google_drive import GoogleDriveClient

_LOGGER = logging.getLogger(__name__)


class BackupGuardianCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Backup Guardian data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._google_drive_client: GoogleDriveClient | None = None
        self._google_drive_enabled = False

    async def async_setup_google_drive(self, config_data: dict) -> bool:
        """Setup Google Drive client if enabled."""
        self._google_drive_enabled = config_data.get(CONF_GOOGLE_DRIVE_ENABLED, False)
        
        if not self._google_drive_enabled:
            _LOGGER.info("Google Drive integration disabled")
            self._google_drive_client = None
            return True

        try:
            credentials = {
                "client_id": config_data.get(CONF_GOOGLE_CLIENT_ID),
                "client_secret": config_data.get(CONF_GOOGLE_CLIENT_SECRET),
                "folder_id": config_data.get(CONF_GOOGLE_FOLDER_ID, "root"),
                "token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("access_token"),
                "refresh_token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("refresh_token"),
            }

            if not all([credentials["client_id"], credentials["client_secret"], credentials["token"]]):
                _LOGGER.error("Missing Google Drive credentials")
                return False

            self._google_drive_client = GoogleDriveClient(self.hass, credentials)
            
            if not await self._google_drive_client.async_setup():
                _LOGGER.error("Failed to setup Google Drive client")
                self._google_drive_client = None
                return False

            _LOGGER.info("Google Drive integration enabled successfully")
            return True

        except Exception as err:
            _LOGGER.error(f"Error setting up Google Drive: {err}", exc_info=True)
            self._google_drive_client = None
            return False

    async def _get_backups_from_supervisor(self) -> list:
        """Get backups using Supervisor via hassio component."""
        try:
            # Verifica che siamo su Hassio/Supervisor
            if not hassio.is_hassio(self.hass):
                _LOGGER.error("This integration requires Home Assistant OS or Supervised")
                return []
            
            # Accedi direttamente al componente hassio
            if "hassio" not in self.hass.data:
                _LOGGER.error("Hassio component not loaded")
                return []
            
            hassio_component = self.hass.data["hassio"]
            
            # Chiama il metodo send_command del componente hassio
            _LOGGER.debug("Calling Supervisor via hassio component")
            
            try:
                result = await hassio_component.send_command(
                    "/backups",
                    method="get",
                    timeout=30
                )
                
                if not result:
                    _LOGGER.error("No response from Supervisor")
                    return []
                
                _LOGGER.debug(f"Supervisor raw response structure: {type(result)}, keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
                
                # Il formato della risposta del Supervisor varia
                backups = []
                
                # Prova diversi formati di risposta
                if isinstance(result, dict):
                    if "data" in result and "backups" in result["data"]:
                        backups = result["data"]["backups"]
                    elif "backups" in result:
                        backups = result["backups"]
                
                _LOGGER.info(f"Retrieved {len(backups)} backups from Supervisor")
                
                # Log del primo backup per debug
                if backups:
                    _LOGGER.debug(f"First backup sample: {backups[0]}")
                
                return backups
                
            except Exception as api_err:
                _LOGGER.error(f"Supervisor API call failed: {api_err}", exc_info=True)
                return []
                    
        except Exception as err:
            _LOGGER.error(f"Error getting backups from Supervisor: {err}", exc_info=True)
            return []

    def _calculate_hash_from_slug(self, slug: str) -> str:
        """Calculate a hash from backup slug for identification."""
        try:
            return hashlib.sha256(slug.encode()).hexdigest()
        except Exception:
            return "N/A"

    def _process_backup(self, backup_data: dict, source: str = "local") -> dict | None:
        """Process a single backup from API data.
        
        Args:
            backup_data: Raw backup data from API
            source: Source/destination of backup (local, google_drive, dropbox, etc.)
        
        Returns:
            Processed backup dictionary with all fields
        """
        try:
            # Data dal Supervisor è in formato ISO UTC
            date_str = backup_data.get("date", "")
            
            try:
                # Formato: "2026-01-31T10:30:00.123456+00:00" (UTC)
                # Convertiamo in datetime UTC
                if "T" in date_str:
                    date_obj_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                elif " " in date_str:
                    date_obj_utc = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    # Assumiamo sia UTC se non ha timezone
                    date_obj_utc = date_obj_utc.replace(tzinfo=ZoneInfo("UTC"))
                else:
                    date_obj_utc = datetime.strptime(date_str, "%Y-%m-%d")
                    date_obj_utc = date_obj_utc.replace(tzinfo=ZoneInfo("UTC"))
                
                # Convertiamo da UTC al fuso orario locale di Home Assistant
                date_obj_local = dt_util.as_local(date_obj_utc)
                
                _LOGGER.debug(f"Backup date conversion: UTC={date_obj_utc.isoformat()} -> Local={date_obj_local.isoformat()}")
                
            except Exception as date_err:
                _LOGGER.debug(f"Could not parse date {date_str}: {date_err}")
                # Fallback: usa l'ora corrente locale
                date_obj_local = dt_util.now()
            
            # Gestisci la dimensione - può essere in diversi formati
            size_bytes = backup_data.get("size", 0)
            
            # Debug del formato size
            _LOGGER.debug(f"Backup size raw value: {size_bytes}, type: {type(size_bytes)}")
            
            # Converti in float
            if isinstance(size_bytes, str):
                # Rimuovi caratteri non numerici e converti
                size_bytes = float(''.join(c for c in size_bytes if c.isdigit() or c == '.'))
            else:
                size_bytes = float(size_bytes)
            
            # Se la dimensione è troppo piccola, potrebbe essere già in MB
            if size_bytes < 1024:
                # È probabilmente già in MB
                size_mb = round(size_bytes, 2)
                size_bytes = int(size_bytes * 1024 * 1024)
            else:
                # È in bytes
                size_mb = round(size_bytes / (1024 * 1024), 2)
                size_bytes = int(size_bytes)
            
            # Nome del backup
            name = backup_data.get("name", backup_data.get("slug", "Unknown"))
            
            # Determina il nome friendly della destinazione
            destination_map = {
                "local": "Home Assistant Locale",
                "google_drive": "Google Drive",
                "dropbox": "Dropbox",
                "onedrive": "OneDrive",
                "nas": "NAS",
                "ftp": "FTP",
            }
            destination_friendly = destination_map.get(source, source.title())
            
            result = {
                "name": name,
                "slug": backup_data.get("slug", ""),
                "size": size_bytes,
                "size_mb": size_mb,
                "date": date_obj_local.strftime("%Y-%m-%d"),
                "time": date_obj_local.strftime("%H:%M:%S"),
                "datetime": date_obj_local,
                "hash": self._calculate_hash_from_slug(backup_data.get("slug", "")),
                "type": backup_data.get("type", "full"),
                "protected": backup_data.get("protected", False),
                "compressed": True,
                "destination": source,  # Codice destinazione (local, google_drive, ecc.)
                "destination_name": destination_friendly,  # Nome user-friendly
            }
            
            _LOGGER.debug(f"Processed backup: {name}, size: {size_mb} MB, time: {date_obj_local.strftime('%H:%M:%S')}, destination: {destination_friendly}")
            return result
            
        except Exception as err:
            _LOGGER.error(f"Error processing backup: {err}, data: {backup_data}", exc_info=True)
            return None

    async def _async_update_data(self) -> dict:
        """Fetch data from Supervisor API and Google Drive."""
        try:
            # Ottieni i backup dal Supervisor (locale)
            backups_raw = await self._get_backups_from_supervisor()
            
            # Processa ogni backup locale
            backups = []
            for backup_raw in backups_raw:
                backup_info = self._process_backup(backup_raw, source="local")
                if backup_info:
                    backups.append(backup_info)
            
            # Ottieni backup da Google Drive se abilitato
            if self._google_drive_enabled and self._google_drive_client:
                try:
                    _LOGGER.debug("Fetching backups from Google Drive...")
                    drive_backups = await self._google_drive_client.async_get_backups()
                    
                    if drive_backups:
                        _LOGGER.info(f"Found {len(drive_backups)} backups on Google Drive")
                        # I backup da Google Drive sono già processati
                        backups.extend(drive_backups)
                    else:
                        _LOGGER.debug("No backups found on Google Drive")
                        
                except Exception as drive_err:
                    _LOGGER.error(f"Error fetching Google Drive backups: {drive_err}", exc_info=True)
                    # Non bloccare l'update per errori Google Drive
            
            if not backups:
                _LOGGER.info("No backups found from any source")
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                    "local_count": 0,
                    "drive_count": 0,
                }
            
            # Ordina per data (più recente prima)
            backups.sort(key=lambda x: x["datetime"], reverse=True)
            
            # Calcola dimensione totale
            total_size = sum(b["size"] for b in backups)
            total_size_mb = round(total_size / (1024 * 1024), 2)
            
            # Ultimo backup
            last_backup = backups[0]
            
            # Conta backup per sorgente
            local_count = sum(1 for b in backups if b["destination"] == "local")
            drive_count = sum(1 for b in backups if b["destination"] == "google_drive")
            
            _LOGGER.info(f"✅ Loaded {len(backups)} backups total ({local_count} local, {drive_count} Google Drive), total: {total_size_mb} MB")
            
            return {
                "backups": backups,
                "total_backups": len(backups),
                "last_backup": last_backup,
                "total_size": total_size,
                "total_size_mb": total_size_mb,
                "local_count": local_count,
                "drive_count": drive_count,
            }

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}", exc_info=True)
            # Non lanciare UpdateFailed, ritorna dati vuoti
            return {
                "backups": [],
                "total_backups": 0,
                "last_backup": None,
                "total_size": 0,
                "total_size_mb": 0,
                "local_count": 0,
                "drive_count": 0,
            }
