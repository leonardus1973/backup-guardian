import logging
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class BackupGuardianCoordinator(DataUpdateCoordinator):
    """Gestisce il recupero dati tramite le API Backup di HA."""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="Backup Guardian",
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self):
        try:
            # INTERROGA IL SISTEMA DI BACKUP DI HA (Funziona su HA OS)
            backups_info = await self.hass.components.backup.async_get_backups()
            
            if not backups_info:
                return {"backups": [], "total_backups": 0, "last_backup": None, "total_size_mb": 0}

            backups_list = []
            total_size_bytes = 0

            for slug, b in backups_info.items():
                # b.date è già un oggetto datetime o stringa ISO
                dt_obj = datetime.fromisoformat(b.date.replace("Z", "+00:00"))
                size_mb = round(b.size / (1024 * 1024), 2)
                total_size_bytes += b.size

                backups_list.append({
                    "name": b.name,
                    "size_mb": size_mb,
                    "date": dt_obj.strftime("%d/%m/%Y"),
                    "time": dt_obj.strftime("%H:%M:%S"),
                    "datetime": dt_obj,
                    "hash": b.slug, # Lo slug è l'identificativo unico
                    "type": "Locale/Cloud"
                })

            # Ordina per il più recente
            backups_list.sort(key=lambda x: x["datetime"], reverse=True)

            return {
                "backups": backups_list,
                "total_backups": len(backups_list),
                "last_backup": backups_list[0] if backups_list else None,
                "total_size_mb": round(total_size_bytes / (1024 * 1024), 2),
            }

        except Exception as err:
            _LOGGER.error(f"Errore caricamento backup: {err}")
            raise UpdateFailed(f"Errore API Backup: {err}")
