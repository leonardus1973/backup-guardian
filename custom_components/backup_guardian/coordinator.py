"""DataUpdateCoordinator for Backup Guardian."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DESTINATION_LOCAL,
    DESTINATION_GOOGLE_DRIVE,
    DESTINATION_NAMES,
    CONF_GOOGLE_DRIVE_ENABLED,
    CONF_GOOGLE_CLIENT_ID,
    CONF_GOOGLE_CLIENT_SECRET,
    CONF_GOOGLE_FOLDER_ID,
    CONF_GOOGLE_TOKEN,
)
from .google_drive import GoogleDriveClient

_LOGGER = logging.getLogger(__name__)


class BackupGuardianCoordinator(DataUpdateCoordinator):
    """Class to manage fetching backup data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._google_drive_client: GoogleDriveClient | None = None
        self._google_drive_enabled = False

    async def async_setup_google_drive(self, config_data: dict) -> bool:
        """Setup Google Drive client if enabled."""
        self._google_drive_enabled = config_data.get(CONF_GOOGLE_DRIVE_ENABLED, False)
        
        if not self._google_drive_enabled:
            _LOGGER.info("Google Drive integration disabled")
            self._google_drive_client = None
            return True

        try:
            credentials = {
                "client_id": config_data.get(CONF_GOOGLE_CLIENT_ID),
                "client_secret": config_data.get(CONF_GOOGLE_CLIENT_SECRET),
                "folder_id": config_data.get(CONF_GOOGLE_FOLDER_ID, "root"),
                "token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("access_token"),
                "refresh_token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("refresh_token"),
            }

            if not all([credentials["client_id"], credentials["client_secret"], credentials["token"]]):
                _LOGGER.error("Missing Google Drive credentials")
                return False

            self._google_drive_client = GoogleDriveClient(self.hass, credentials)
            
            if not await self._google_drive_client.async_setup():
                _LOGGER.error("Failed to setup Google Drive client")
                self._google_drive_client = None
                return False

            _LOGGER.info("Google Drive integration enabled successfully")
            return True

        except Exception as err:
            _LOGGER.error(f"Error setting up Google Drive: {err}", exc_info=True)
            self._google_drive_client = None
            return False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from all backup sources."""
        try:
            # Fetch local backups
            local_backups = await self._get_local_backups()
            
            # Fetch Google Drive backups if enabled
            drive_backups = []
            if self._google_drive_enabled and self._google_drive_client:
                try:
                    drive_backups = await self._google_drive_client.async_get_backups()
                    _LOGGER.debug(f"Fetched {len(drive_backups)} backups from Google Drive")
                except Exception as err:
                    _LOGGER.error(f"Error fetching Google Drive backups: {err}")

            # Merge and sort
            all_backups = local_backups + drive_backups
            all_backups.sort(key=lambda x: x["datetime"], reverse=True)

            total_size = sum(backup["size_mb"] for backup in all_backups)
            last_backup = all_backups[0] if all_backups else None

            return {
                "backups": all_backups,
                "total_backups": len(all_backups),
                "total_size": round(total_size, 2),
                "last_backup": last_backup,
                "local_count": len(local_backups),
                "drive_count": len(drive_backups),
            }

        except Exception as err:
            _LOGGER.error(f"Error updating backup data: {err}", exc_info=True)
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _get_local_backups(self) -> list[dict[str, Any]]:
        """Get local backups using backup integration."""
        try:
            # Use the backup integration directly
            backup_platform = self.hass.data.get("backup")
            
            if backup_platform:
                _LOGGER.debug("Using backup platform from hass.data")
                
                # Try to get backups list
                try:
                    backups_info = await backup_platform.async_get_backups()
                    
                    if backups_info:
                        _LOGGER.info(f"Found {len(backups_info)} local backups via backup platform")
                        
                        backups = []
                        for backup_id, backup_data in backups_info.backups.items():
                            converted = {
                                "slug": backup_id,
                                "name": backup_data.name,
                                "date": backup_data.date.isoformat(),
                                "size": backup_data.size,
                                "type": "full",
                                "protected": backup_data.protected,
                                "compressed": True,
                            }
                            backup_info = self._process_backup(converted, source=DESTINATION_LOCAL)
                            if backup_info:
                                backups.append(backup_info)
                        
                        return backups
                except AttributeError:
                    _LOGGER.debug("backup platform doesn't have async_get_backups")

            _LOGGER.warning("Could not access backup platform")
            return []

        except Exception as err:
            _LOGGER.error(f"Error fetching local backups: {err}", exc_info=True)
            return []

    def _process_backup(self, backup_data: dict, source: str = DESTINATION_LOCAL) -> dict[str, Any] | None:
        """Process a backup into standard format."""
        try:
            name = backup_data.get("name", "Unknown")
            slug = backup_data.get("slug", "")
            size_bytes = backup_data.get("size", 0)
            backup_type = backup_data.get("type", "full")
            protected = backup_data.get("protected", False)
            compressed = backup_data.get("compressed", True)

            # Parse date
            date_str = backup_data.get("date")
            if not date_str:
                date_obj = dt_util.now()
            else:
                try:
                    date_str_clean = date_str.replace("Z", "+00:00")
                    date_obj_utc = datetime.fromisoformat(date_str_clean)
                    date_obj = dt_util.as_local(date_obj_utc)
                except (ValueError, AttributeError):
                    date_obj = dt_util.now()

            size_mb = round(size_bytes / (1024 * 1024), 2)
            backup_hash = backup_data.get("content", {}).get("homeassistant", slug)
            destination_name = DESTINATION_NAMES.get(source, source)

            return {
                "name": name,
                "slug": slug,
                "size": size_bytes,
                "size_mb": size_mb,
                "date": date_obj.strftime("%Y-%m-%d"),
                "time": date_obj.strftime("%H:%M:%S"),
                "datetime": date_obj,
                "hash": backup_hash,
                "type": backup_type,
                "protected": protected,
                "compressed": compressed,
                "destination": source,
                "destination_name": destination_name,
            }

        except Exception as err:
            _LOGGER.error(f"Error processing backup: {err}", exc_info=True)
            return None
            
            
