"""The Backup Guardian integration."""
import logging
import os
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import BackupGuardianCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Backup Guardian from a config entry."""
    # Copy frontend files automatically
    await _copy_frontend_files(hass)
    
    # Initialize coordinator
    coordinator = BackupGuardianCoordinator(hass)
    
    # Setup Google Drive if enabled
    google_drive_ok = await coordinator.async_setup_google_drive(entry.data)
    if not google_drive_ok:
        _LOGGER.warning(
            "Google Drive setup failed, continuing with local backups only"
        )
    
    # First refresh to get data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for config changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _copy_frontend_files(hass: HomeAssistant) -> None:
    """Copy frontend JavaScript files to www directory."""
    try:
        # Directory sorgente (dove si trova il file nell'integrazione)
        source_dir = Path(__file__).parent / "www"
        source_file = source_dir / "backup-guardian-card.js"
        
        # Directory destinazione (dove deve essere copiato per HACS/frontend)
        dest_dir = Path(hass.config.path("www/community/backup_guardian"))
        dest_file = dest_dir / "backup-guardian-card.js"
        
        # Crea la directory di destinazione se non esiste
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copia il file se non esiste o se è diverso
        if not dest_file.exists() or _files_are_different(source_file, dest_file):
            await hass.async_add_executor_job(shutil.copy2, source_file, dest_file)
            _LOGGER.info(f"✅ Frontend file copied to {dest_file}")
        else:
            _LOGGER.debug("Frontend file already up to date")
            
    except Exception as err:
        _LOGGER.warning(f"Could not copy frontend files: {err}. You may need to copy them manually.")


def _files_are_different(file1: Path, file2: Path) -> bool:
    """Check if two files are different."""
    try:
        # Confronta dimensioni prima (veloce)
        if file1.stat().st_size != file2.stat().st_size:
            return True
        
        # Se le dimensioni sono uguali, confronta il contenuto (più lento ma sicuro)
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() != f2.read()
    except Exception:
        # In caso di errore, assumiamo che siano diversi per forzare la copia
        return True
