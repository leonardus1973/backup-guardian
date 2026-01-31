"""Sensor platform for Backup Guardian."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ATTR_BACKUP_NAME,
    ATTR_BACKUP_DATE,
    ATTR_BACKUP_TIME,
    ATTR_BACKUP_SIZE,
    ATTR_BACKUP_HASH,
    ATTR_BACKUP_TYPE,
    ATTR_BACKUP_LIST,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Backup Guardian sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        BackupGuardianLastBackupSensor(coordinator, entry),
        BackupGuardianTotalBackupsSensor(coordinator, entry),
        BackupGuardianTotalSizeSensor(coordinator, entry),
    ]

    async_add_entities(sensors)


class BackupGuardianLastBackupSensor(CoordinatorEntity, SensorEntity):
    """Sensor for the last backup."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Ultimo Backup"
        self._attr_unique_id = f"{entry.entry_id}_last_backup"
        self._attr_icon = "mdi:backup-restore"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data and self.coordinator.data.get("last_backup"):
            last = self.coordinator.data["last_backup"]
            return f"{last['date']} {last['time']}"
        return "Nessun backup"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data and self.coordinator.data.get("last_backup"):
            last = self.coordinator.data["last_backup"]
            return {
                ATTR_BACKUP_NAME: last["name"],
                ATTR_BACKUP_DATE: last["date"],
                ATTR_BACKUP_TIME: last["time"],
                ATTR_BACKUP_SIZE: f"{last['size_mb']} MB",
                ATTR_BACKUP_HASH: last["hash"],
                ATTR_BACKUP_TYPE: last["type"],
            }
        return {}


class BackupGuardianTotalBackupsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total number of backups."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Totale Backup"
        self._attr_unique_id = f"{entry.entry_id}_total_backups"
        self._attr_icon = "mdi:counter"
        self._attr_native_unit_of_measurement = "backup"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_backups", 0)
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data and self.coordinator.data.get("backups"):
            backups = self.coordinator.data["backups"]
            backup_list = []
            for backup in backups:
                backup_list.append({
                    "name": backup["name"],
                    "date": backup["date"],
                    "time": backup["time"],
                    "size": f"{backup['size_mb']} MB",
                    "hash": backup["hash"],
                })
            return {ATTR_BACKUP_LIST: backup_list}
        return {}


class BackupGuardianTotalSizeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total size of all backups."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Dimensione Totale Backup"
        self._attr_unique_id = f"{entry.entry_id}_total_size"
        self._attr_icon = "mdi:harddisk"
        self._attr_native_unit_of_measurement = "MB"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_size_mb", 0)
        return 0
