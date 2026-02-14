"""Data coordinator for Backup Guardian."""
import hashlib
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import hassio
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_INTERVAL

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

    def _process_backup(self, backup_data: dict) -> dict | None:
        """Process a single backup from API data."""
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
            }
            
            _LOGGER.debug(f"Processed backup: {name}, size: {size_mb} MB, time: {date_obj_local.strftime('%H:%M:%S')}")
            return result
            
        except Exception as err:
            _LOGGER.error(f"Error processing backup: {err}, data: {backup_data}", exc_info=True)
            return None

    async def _async_update_data(self) -> dict:
        """Fetch data from Supervisor API."""
        try:
            # Ottieni i backup dal Supervisor
            backups_raw = await self._get_backups_from_supervisor()
            
            if not backups_raw:
                _LOGGER.info("No backups found")
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                }
            
            # Processa ogni backup
            backups = []
            for backup_raw in backups_raw:
                backup_info = self._process_backup(backup_raw)
                if backup_info:
                    backups.append(backup_info)
            
            if not backups:
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                }
            
            # Ordina per data (più recente prima)
            backups.sort(key=lambda x: x["datetime"], reverse=True)
            
            # Calcola dimensione totale
            total_size = sum(b["size"] for b in backups)
            total_size_mb = round(total_size / (1024 * 1024), 2)
            
            # Ultimo backup
            last_backup = backups[0]
            
            _LOGGER.info(f"✅ Loaded {len(backups)} backups, total: {total_size_mb} MB")
            
            return {
                "backups": backups,
                "total_backups": len(backups),
                "last_backup": last_backup,
                "total_size": total_size,
                "total_size_mb": total_size_mb,
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
            }
