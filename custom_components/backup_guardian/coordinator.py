"""Data coordinator for Backup Guardian."""
import hashlib
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL, BACKUP_PATHS

_LOGGER = logging.getLogger(__name__)


class BackupGuardianCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Backup Guardian data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.backup_path = self._find_backup_path()

    def _find_backup_path(self) -> Path | None:
        """Find the correct backup path."""
        for path_str in BACKUP_PATHS:
            path = Path(path_str)
            if path.exists():
                _LOGGER.info(f"Found backup directory: {path}")
                return path
        
        _LOGGER.warning(f"No backup directory found. Tried: {BACKUP_PATHS}")
        return None

    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of a file."""
        try:
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                # Leggi il file in blocchi per non sovraccaricare la memoria
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as err:
            _LOGGER.error(f"Error calculating hash for {filepath}: {err}")
            return "N/A"

    def _get_backup_info(self, filepath: Path) -> dict:
        """Get information about a single backup file."""
        try:
            stat = filepath.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            return {
                "name": filepath.name,
                "path": str(filepath),
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "date": modified_time.strftime("%Y-%m-%d"),
                "time": modified_time.strftime("%H:%M:%S"),
                "datetime": modified_time,
                "hash": self._calculate_file_hash(filepath),
                "type": "local",
                "protected": False,  # Può essere esteso in futuro
                "compressed": filepath.suffix == ".tar",
            }
        except Exception as err:
            _LOGGER.error(f"Error getting info for {filepath}: {err}")
            return None

    async def _async_update_data(self) -> dict:
        """Fetch data from backup directory."""
        try:
            # Verifica che il percorso esista
            if not self.backup_path or not self.backup_path.exists():
                _LOGGER.warning(f"Backup path not available")
                return {
                    "backups": [],
                    "total_backups": 0,
                    "last_backup": None,
                    "total_size": 0,
                    "total_size_mb": 0,
                }

            # Ottieni tutti i file .tar dalla directory dei backup
            backup_files = list(self.backup_path.glob("*.tar"))
            
            _LOGGER.debug(f"Found {len(backup_files)} backup files in {self.backup_path}")
            
            # Ottieni informazioni su ogni backup
            backups = []
            for backup_file in backup_files:
                info = await self.hass.async_add_executor_job(
                    self._get_backup_info, backup_file
                )
                if info:
                    backups.append(info)

            # Ordina i backup per data (più recente prima)
            backups.sort(key=lambda x: x["datetime"], reverse=True)

            # Calcola la dimensione totale
            total_size = sum(b["size"] for b in backups)
            total_size_mb = round(total_size / (1024 * 1024), 2)

            # Ottieni l'ultimo backup
            last_backup = backups[0] if backups else None

            return {
                "backups": backups,
                "total_backups": len(backups),
                "last_backup": last_backup,
                "total_size": total_size,
                "total_size_mb": total_size_mb,
            }

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}")
            raise UpdateFailed(f"Error communicating with backup directory: {err}")

