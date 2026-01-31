"""Data coordinator for Backup Guardian."""
import logging
from datetime import datetime, timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.components import backup  # Utilizziamo il componente nativo

from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class BackupGuardianCoordinator(DataUpdateCoordinator):
    """Gestisce il recupero dati tramite le API Backup di HA."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Recupera i dati dei backup dal sistema."""
        try:
            # Recupera i backup registrati in HA (Locali e Cloud se integrati)
            manager = await self.hass.components.backup.async_get_backups()
            
            backups = []
            total_size = 0

            for slug, b in manager.items():
                # Formattiamo la data
                # b.date è solitamente una stringa ISO o un oggetto datetime
                dt_obj = datetime.fromisoformat(b.date.replace("Z", "+00:00"))
                
                size_mb = round(b.size / (1024 * 1024), 2)
                total_size += b.size

                backups.append({
                    "name": b.name,
                    "size_mb": size_mb,
                    "date": dt_obj.strftime("%Y-%m-%d"),
                    "time": dt_obj.strftime("%H:%M:%S"),
                    "datetime": dt_obj,
                    "hash": b.slug, # Usiamo lo slug come identificativo/hash
                    "type": "Locale", # Estensibile in futuro
                })

            # Ordina per il più recente
            backups.sort(key=lambda x: x["datetime"], reverse=True)

            total_size_mb = round(total_size / (1024 * 1024), 2)
            last_backup = backups[0] if backups else None

            return {
                "backups": backups,
                "total_backups": len(backups),
                "last_backup": last_backup,
                "total_size": total_size,
                "total_size_mb": total_size_mb,
            }

        except Exception as err:
            _LOGGER.error(f"Errore durante l'aggiornamento dei backup: {err}")
            raise UpdateFailed(f"Impossibile leggere i backup: {err}")
