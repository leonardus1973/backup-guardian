"""Backup Guardian Integration."""
import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

# Il dominio deve corrispondere al nome della cartella
DOMAIN = "backup_guardian"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configurazione tramite file configuration.yaml (opzionale)."""
    
    # REGISTRAZIONE DELLA CARD:
    # Questo espone la cartella 'www' del tuo custom_component 
    # all'indirizzo web: /backup_guardian/backup-guardian-card.js
    dist_dir = hass.config.path(f"custom_components/{DOMAIN}/www")
    
    if os.path.isdir(dist_dir):
        hass.http.register_static_path(
            f"/{DOMAIN}",
            dist_dir,
            cache_headers=False
        )
        _LOGGER.info("Percorso statico per Backup Guardian Card registrato correttamente")
    else:
        _LOGGER.error(f"Cartella www non trovata in {dist_dir}")

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurazione tramite Interfaccia Utente (Config Flow)."""
    
    # Carica la piattaforma sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Rimozione dell'integrazione."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
