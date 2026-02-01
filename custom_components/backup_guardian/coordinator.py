"""Data coordinator for Backup Guardian."""
import hashlib
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import hassio

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
        """Get backups using Supervisor REST API."""
        try:
            # Verifica che siamo su Hassio/Supervisor (usando il metodo corretto)
            if not hassio.is_hassio(self.hass):
                _LOGGER.error("This integration requires Home Assistant OS or Supervised")
                return []
            
            # Ottieni il client del Supervisor
            supervisor_client = hassio.get_supervisor_client(self.hass)
            if not supervisor_client:
                _LOGGER.error("Could not get Supervisor client")
                return []
            
            # Chiama l'API del Supervisor per ottenere i backup
            _LOGGER.debug("Calling Supervisor API for backups")
            
            try:
                # Usa il metodo del client per ottenere i backup
                response = await supervisor_client.get("/backups")
                
                if not response:
                    _LOGGER.error("No response from Supervisor")
                    return []
                
                _LOGGER.debug(f"Supervisor response: {response}")
                
                # Il formato della risposta del Supervisor
                backups = response.get("backups", [])
                _LOGGER.info(f"Retrieved {len(backups)} backups from Supervisor")
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
            # Data dal Supervisor è in formato ISO
            date_str = backup_data.get("date", "")
            try:
                # Formato: "2024-01-31T10:30:00.123456+00:00"
                date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except Exception:
                try:
                    # Prova formato semplice
                    date_obj = datetime.strptime(date_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                except Exception:
                    _LOGGER.debug(f"Could not parse date: {date_str}")
                    date_obj = datetime.now()
            
            # Size è in bytes (float)
            size_bytes = float(backup_data.get("size", 0))
            size_mb = round(size_bytes / (1024 * 1024), 2)
            
            # Nome del backup
            name = backup_data.get("name", backup_data.get("slug", "Unknown"))
            
            return {
                "name": name,
                "slug": backup_data.get("slug", ""),
                "size": int(size_bytes),
                "size_mb": size_mb,
                "date": date_obj.strftime("%Y-%m-%d"),
                "time": date_obj.strftime("%H:%M:%S"),
                "datetime": date_obj,
                "hash": self._calculate_hash_from_slug(backup_data.get("slug", "")),
                "type": backup_data.get("type", "full"),
                "protected": backup_data.get("protected", False),
                "compressed": True,
            }
        except Exception as err:
            _LOGGER.error(f"Error processing backup: {err}, data: {backup_data}")
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
            # Non lanciare UpdateFailed se è il primo caricamento
            return {
                "backups": [],
                "total_backups": 0,
                "last_backup": None,
                "total_size": 0,
                "total_size_mb": 0,
            }


