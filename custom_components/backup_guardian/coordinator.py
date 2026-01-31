"""Data coordinator for Backup Guardian."""
import hashlib
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

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
        """Get backups using Home Assistant Supervisor API via REST."""
        try:
            # Usa il client HTTP di HA
            session = async_get_clientsession(self.hass)
            
            # Endpoint API del Supervisor per i backup
            url = "http://supervisor/backups"
            
            # Header con il token del Supervisor (HA gestisce automaticamente)
            headers = {
                "Authorization": f"Bearer {self.hass.data.get('hassio_token', '')}",
            }
            
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    backups = data.get("data", {}).get("backups", [])
                    _LOGGER.debug(f"Retrieved {len(backups)} backups from Supervisor API")
                    return backups
                else:
                    _LOGGER.warning(f"Supervisor API returned status {response.status}")
                    return []
                    
        except Exception as err:
            _LOGGER.error(f"Error getting backups from Supervisor API: {err}")
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
                _LOGGER.warning(f"Could not parse date {date_str}: {date_err}")
                date_obj = datetime.now()
            
            # Converti size da bytes a MB
            size_bytes = backup_data.get("size", 0)
            # Size potrebbe essere in formato stringa con unità
            if isinstance(size_bytes, str):
                try:
                    # Rimuovi eventuali caratteri non numerici
                    size_bytes = float(''.join(filter(str.isdigit, size_bytes)))
                except:
                    size_bytes = 0
            
            size_mb = round(float(size_bytes) / (1024 * 1024), 2) if size_bytes else 0
            
            return {
                "name": backup_data.get("name", "Unknown"),
                "slug": backup_data.get("slug", ""),
                "size": int(size_bytes),
                "size_mb": size_mb,
                "date": date_obj.strftime("%Y-%m-%d"),
                "time": date_obj.strftime("%H:%M:%S"),
                "datetime": date_obj,
                "hash": self._calculate_hash_from_slug(backup_data.get("slug", "")),
                "type": backup_data.get("type", "local"),
                "protected": backup_data.get("protected", False),
                "compressed": backup_data.get("compressed", True),
            }
        except Exception as err:
            _LOGGER.error(f"Error processing backup data: {err}, data: {backup_data}")
            return None

    async def _async_update_data(self) -> dict:
        """Fetch data from Home Assistant Supervisor API."""
        try:
            # Verifica che siamo su Home Assistant OS/Supervised
            if "hassio_token" not in self.hass.data:
                _LOGGER.warning("Supervisor not available - this integration requires Home Assistant OS or Supervised")
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                }
            
            # Ottieni i backup dall'API
            backups_raw = await self._get_backups_from_supervisor()
            
            if not backups_raw:
                _LOGGER.info("No backups found via Supervisor API")
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
            raise UpdateFailed(f"Error communicating with Supervisor API: {err}")

        

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}")
            raise UpdateFailed(f"Error communicating with backup directory: {err}")

