"""Backup Guardian Integration."""
import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .coordinator import BackupGuardianCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Backup Guardian from a config entry."""
    
    # 1. Registra il percorso statico per la card Lovelace
    # Questo permette di usare l'URL: /backup_guardian/backup-guardian-card.js
    dist_dir = hass.config.path(f"custom_components/{DOMAIN}/www")
    if os.path.isdir(dist_dir):
        hass.http.register_static_path(
            f"/{DOMAIN}",
            dist_dir,
            cache_headers=False
        )
    
    # 2. Inizializza il Coordinator
    coordinator = BackupGuardianCoordinator(hass)
    
    # Forza il primo aggiornamento dati
    await coordinator.async_config_entry_first_refresh()
    
    # 3. Salva il coordinator per l'uso nei sensori
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # 4. Carica la piattaforma sensore
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


