import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .coordinator import BackupGuardianCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configurazione all'avvio di Home Assistant."""
    # REGISTRAZIONE STATICA: viene eseguita ad ogni boot
    dist_dir = hass.config.path(f"custom_components/{DOMAIN}/www")
    
    if os.path.isdir(dist_dir):
        hass.http.register_static_path(
            f"/{DOMAIN}",
            dist_dir,
            cache_headers=False
        )
        _LOGGER.info(f"Percorso statico /{DOMAIN} registrato correttamente")
    else:
        _LOGGER.error(f"Cartella www non trovata in {dist_dir}")
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurazione quando l'integrazione viene aggiunta dall'interfaccia."""
    coordinator = BackupGuardianCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
    

