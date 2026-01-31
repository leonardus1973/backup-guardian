"""Backup Guardian Integration per Home Assistant."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Backup Guardian component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Backup Guardian from a config entry."""
    _LOGGER.info("Setting up Backup Guardian")
    
    # Importa il coordinator
    from .coordinator import BackupGuardianCoordinator
    
    # Crea il coordinator per aggiornare i dati
    coordinator = BackupGuardianCoordinator(hass)
    
    # Primo refresh dei dati
    await coordinator.async_config_entry_first_refresh()
    
    # Salva il coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Setup delle piattaforme (sensori)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload delle piattaforme
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
