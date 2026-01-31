import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ATTR_BACKUP_LIST, ATTR_BACKUP_NAME, ATTR_BACKUP_DATE, ATTR_BACKUP_TIME, ATTR_BACKUP_SIZE, ATTR_BACKUP_HASH

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BackupGuardianLastBackupSensor(coordinator, entry),
        BackupGuardianTotalBackupsSensor(coordinator, entry),
        BackupGuardianTotalSizeSensor(coordinator, entry),
    ])

class BackupGuardianLastBackupSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_name = "Backup Guardian Ultimo Backup"
        self._attr_unique_id = f"{entry.entry_id}_last_backup"
        self._attr_icon = "mdi:backup-restore"

    @property
    def state(self):
        last = self.coordinator.data.get("last_backup")
        return f"{last['date']} {last['time']}" if last else "Nessun backup"

    @property
    def extra_state_attributes(self):
        last = self.coordinator.data.get("last_backup")
        if not last: return {}
        return {
            ATTR_BACKUP_NAME: last["name"],
            ATTR_BACKUP_DATE: last["date"],
            ATTR_BACKUP_TIME: last["time"],
            ATTR_BACKUP_SIZE: f"{last['size_mb']} MB",
            ATTR_BACKUP_HASH: last["hash"],
        }

class BackupGuardianTotalBackupsSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_name = "Backup Guardian Totale Backup"
        self._attr_unique_id = f"{entry.entry_id}_total_backups"
        self._attr_icon = "mdi:counter"

    @property
    def state(self):
        return self.coordinator.data.get("total_backups", 0)

    @property
    def extra_state_attributes(self):
        backups = self.coordinator.data.get("backups", [])
        return {ATTR_BACKUP_LIST: [
            {"name": b["name"], "date": b["date"], "time": b["time"], "size": f"{b['size_mb']} MB", "hash": b["hash"]}
            for b in backups
        ]}

class BackupGuardianTotalSizeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_name = "Backup Guardian Dimensione Totale"
        self._attr_unique_id = f"{entry.entry_id}_total_size"
        self._attr_icon = "mdi:harddisk"
        self._attr_native_unit_of_measurement = "MB"

    @property
    def state(self):
        return self.coordinator.data.get("total_size_mb", 0)

