"""Sensor platform for Backup Guardian."""
import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

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

# Leggi la versione dal manifest
import json
from pathlib import Path

def get_version() -> str:
    """Get version from manifest."""
    try:
        manifest_path = Path(__file__).parent / "manifest.json"
        with open(manifest_path) as f:
            manifest = json.load(f)
        return manifest.get("version", "unknown")
    except Exception:
        return "unknown"

VERSION = get_version()


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

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Ultimo Backup"
        self._attr_unique_id = f"{entry.entry_id}_ultimo_backup"
        self._attr_icon = "mdi:backup-restore"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Backup Guardian",
            manufacturer="Leonardo",
            model="Backup Monitor",
            sw_version=VERSION,
        )

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

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Totale Backup"
        self._attr_unique_id = f"{entry.entry_id}_totale_backup"
        self._attr_icon = "mdi:counter"
        self._attr_native_unit_of_measurement = "backup"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Backup Guardian",
            manufacturer="Leonardo",
            model="Backup Monitor",
            sw_version=VERSION,
        )

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

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Dimensione Totale"
        self._attr_unique_id = f"{entry.entry_id}_dimensione_totale"
        self._attr_icon = "mdi:harddisk"
        self._attr_native_unit_of_measurement = "MB"
        self._attr_device_class = SensorDeviceClass.DATA_SIZE

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Backup Guardian",
            manufacturer="Leonardo",
            model="Backup Monitor",
            sw_version=VERSION,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("total_size_mb", 0)
        return 0
