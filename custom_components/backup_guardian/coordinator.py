"""Data coordinator for Backup Guardian."""
import hashlib
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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

    async def _get_backups_from_service(self) -> list:
        """Get backups using Home Assistant backup service."""
        try:
            # Usa il servizio backup.info per ottenere i dati
            service_data = await self.hass.services.async_call(
                "backup",
                "info",
                {},
                blocking=True,
                return_response=True,
            )
            
            if service_data and "backups" in service_data:
                backups = service_data["backups"]
                _LOGGER.info(f"Retrieved {len(backups)} backups from backup service")
                return backups
            
            _LOGGER.warning("No backups data in service response")
            return []
            
        except Exception as err:
            _LOGGER.error(f"Error calling backup service: {err}", exc_info=True)
            # Prova metodo alternativo
            return await self._get_backups_alternative()

    async def _get_backups_alternative(self) -> list:
        """Alternative method using hassio component."""
        try:
            # Verifica se hassio è disponibile
            if "hassio" not in self.hass.data:
                _LOGGER.error("Hassio component not available")
                return []
            
            hassio = self.hass.data["hassio"]
            
            # Chiama l'API per ottenere i backup
            result = await hassio.send_command("/backups", method="get")
            
            if result and "backups" in result.get("data", {}):
                backups = result["data"]["backups"]
                _LOGGER.info(f"Retrieved {len(backups)} backups via hassio API")
                return backups
            
            _LOGGER.warning("No backups in hassio response")
            return []
            
        except Exception as err:
            _LOGGER.error(f"Error using hassio API: {err}", exc_info=True)
            return []

    def _calculate_hash_from_slug(self, slug: str) -> str:
        """Calculate a hash from backup slug for identification."""
        try:
            return hashlib.sha256(slug.encode()).hexdigest()
        except Exception as err:
            _LOGGER.error(f"Error calculating hash: {err}")
            return "N/A"

    def _process_backup(self, backup_data: dict) -> dict:
        """Process a single backup from API data."""
        try:
            # Converti il timestamp in datetime
            date_str = backup_data.get("date", "")
            try:
                # Prova diversi formati di data
                if "T" in date_str:
                    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                else:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except Exception as date_err:
                _LOGGER.debug(f"Could not parse date {date_str}: {date_err}")
                date_obj = datetime.now()
            
            # Converti size da bytes a MB
            size_bytes = backup_data.get("size", 0)
            # Size potrebbe essere già in MB o in formato stringa
            if isinstance(size_bytes, str):
                try:
                    size_bytes = float(''.join(filter(lambda x: x.isdigit() or x == '.', size_bytes)))
                except:
                    size_bytes = 0
            
            size_mb = round(float(size_bytes) / (1024 * 1024), 2) if size_bytes > 1024 else round(float(size_bytes), 2)
            
            backup_name = backup_data.get("name", backup_data.get("slug", "Unknown"))
            
            return {
                "name": backup_name,
                "slug": backup_data.get("slug", ""),
                "size": int(size_bytes) if size_bytes > 1024 else int(size_bytes * 1024 * 1024),
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
            _LOGGER.error(f"Error processing backup: {err}, data: {backup_data}", exc_info=True)
            return None

    async def _async_update_data(self) -> dict:
        """Fetch data from Home Assistant backup service."""
        try:
            # Ottieni i backup dal servizio
            backups_raw = await self._get_backups_from_service()
            
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
                _LOGGER.warning("No valid backups after processing")
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                }
            
            # Ordina i backup per data (più recente prima)
            backups.sort(key=lambda x: x["datetime"], reverse=True)
            
            # Calcola la dimensione totale
            total_size = sum(b["size"] for b in backups)
            total_size_mb = round(total_size / (1024 * 1024), 2)
            
            # Ottieni l'ultimo backup
            last_backup = backups[0] if backups else None
            
            _LOGGER.info(f"Successfully loaded {len(backups)} backups, total size: {total_size_mb} MB")
            
            return {
                "backups": backups,
                "total_backups": len(backups),
                "last_backup": last_backup,
                "total_size": total_size,
                "total_size_mb": total_size_mb,
            }

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}", exc_info=True)
            raise UpdateFailed(f"Error fetching backup data: {err}")

        

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}")
            raise UpdateFailed(f"Error communicating with backup directory: {err}")

