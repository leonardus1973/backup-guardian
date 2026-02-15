"""DataUpdateCoordinator for Backup Guardian."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components import hassio
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from homeassistant.exceptions import ConfigEntryNotReady

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
        """Setup Google Drive client if enabled.
        
        Args:
            config_data: Configuration entry data
            
        Returns:
            True if setup successful or not needed, False if failed
        """
        self._google_drive_enabled = config_data.get(CONF_GOOGLE_DRIVE_ENABLED, False)
        
        if not self._google_drive_enabled:
            _LOGGER.info("Google Drive integration disabled")
            self._google_drive_client = None
            return True

        try:
            # Extract Google credentials
            credentials = {
                "client_id": config_data.get(CONF_GOOGLE_CLIENT_ID),
                "client_secret": config_data.get(CONF_GOOGLE_CLIENT_SECRET),
                "folder_id": config_data.get(CONF_GOOGLE_FOLDER_ID, "root"),
                "token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("access_token"),
                "refresh_token": config_data.get(CONF_GOOGLE_TOKEN, {}).get("refresh_token"),
            }

            # Validate we have all required credentials
            if not all([
                credentials["client_id"],
                credentials["client_secret"],
                credentials["token"],
            ]):
                _LOGGER.error("Missing Google Drive credentials")
                return False

            # Initialize Google Drive client
            self._google_drive_client = GoogleDriveClient(self.hass, credentials)
            
            # Setup the client
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
        """Fetch data from Supervisor API and Google Drive."""
        try:
            # Fetch local backups from Supervisor
            local_backups = await self._get_backups_from_supervisor()
            
            # Fetch Google Drive backups if enabled
            drive_backups = []
            if self._google_drive_enabled and self._google_drive_client:
                try:
                    drive_backups = await self._google_drive_client.async_get_backups()
                    _LOGGER.debug(f"Fetched {len(drive_backups)} backups from Google Drive")
                except Exception as err:
                    _LOGGER.error(f"Error fetching Google Drive backups: {err}")
                    # Don't fail the entire update, just log the error

            # Merge backups from all sources
            all_backups = local_backups + drive_backups
            
            # Sort by date (most recent first)
            all_backups.sort(key=lambda x: x["datetime"], reverse=True)

            # Calculate total size
            total_size = sum(backup["size_mb"] for backup in all_backups)

            # Get last backup
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

    async def _get_backups_from_supervisor(self) -> list[dict[str, Any]]:
        """Get backups from Home Assistant Supervisor API.
        
        Returns:
            List of backup dictionaries
        """
        try:
            # Try to get backups using backup manager (HA 2023.6+)
            try:
                from homeassistant.components.backup import BackupManager
                backup_manager: BackupManager = self.hass.data.get("backup_manager")
                
                if backup_manager:
                    backups_data = await backup_manager.async_get_backups()
                    if backups_data:
                        _LOGGER.debug(f"Found {len(backups_data)} local backups via BackupManager")
                        
                        # Process backups from backup manager
                        backups = []
                        for backup_id, backup_data in backups_data.items():
                            # Convert backup manager format to our format
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
            except (ImportError, AttributeError, KeyError) as e:
                _LOGGER.debug(f"BackupManager not available: {e}, trying hassio API")

            # Fallback: try hassio websocket API
            try:
                websocket = self.hass.components.hassio
                if hasattr(websocket, 'async_get_supervisor_info'):
                    # Try to call supervisor API directly
                    import aiohttp
                    
                    # Get supervisor token
                    supervisor_token = self.hass.data.get("hassio_auth", {}).get("token")
                    if not supervisor_token:
                        _LOGGER.warning("No supervisor token available")
                        return []
                    
                    url = "http://supervisor/backups"
                    headers = {
                        "Authorization": f"Bearer {supervisor_token}",
                        "Content-Type": "application/json",
                    }
                    
                    timeout = aiohttp.ClientTimeout(total=30)
                    async with aiohttp.ClientSession(timeout=timeout) as session:
                        async with session.get(url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                backups_data = data.get("data", {}).get("backups", [])
                                _LOGGER.debug(f"Found {len(backups_data)} local backups via Supervisor API")
                                
                                # Process each backup
                                backups = []
                                for backup_data in backups_data:
                                    backup_info = self._process_backup(backup_data, source=DESTINATION_LOCAL)
                                    if backup_info:
                                        backups.append(backup_info)
                                
                                return backups
                            else:
                                _LOGGER.warning(f"Supervisor API returned status {response.status}")
            except Exception as e:
                _LOGGER.debug(f"Hassio API not available: {e}")

            _LOGGER.warning("No backup source available")
            return []

        except Exception as err:
            _LOGGER.error(f"Error fetching backups from Supervisor: {err}", exc_info=True)
            return []

    def _process_backup(
        self, backup_data: dict, source: str = DESTINATION_LOCAL
    ) -> dict[str, Any] | None:
        """Process a backup from Supervisor API.
        
        Args:
            backup_data: Raw backup data from API
            source: Source of backup (local, google_drive, etc)
            
        Returns:
            Processed backup dictionary or None if invalid
        """
        try:
            # Extract basic info
            name = backup_data.get("name", "Unknown")
            slug = backup_data.get("slug", "")
            size_bytes = backup_data.get("size", 0)
            backup_type = backup_data.get("type", "full")
            protected = backup_data.get("protected", False)
            compressed = backup_data.get("compressed", True)

            # Parse date with timezone conversion
            date_str = backup_data.get("date")
            if not date_str:
                _LOGGER.warning(f"Backup {name} has no date")
                date_obj = dt_util.now()
            else:
                # Parse ISO format date (from Supervisor API)
                # Remove 'Z' and add explicit UTC timezone
                date_str_clean = date_str.replace("Z", "+00:00")
                
                try:
                    # Parse as UTC
                    date_obj_utc = datetime.fromisoformat(date_str_clean)
                    # Convert to local timezone
                    date_obj = dt_util.as_local(date_obj_utc)
                except ValueError as err:
                    _LOGGER.warning(f"Could not parse date {date_str}: {err}")
                    date_obj = dt_util.now()

            # Calculate size in MB
            size_mb = round(size_bytes / (1024 * 1024), 2)

            # Get SHA256 hash for identification (if available)
            backup_hash = backup_data.get("content", {}).get("homeassistant", "")
            if not backup_hash:
                backup_hash = slug  # Fallback to slug

            # Get destination friendly name
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

    async def async_refresh_google_drive_token(self) -> bool:
        """Refresh Google Drive OAuth token if needed.
        
        Returns:
            True if refresh successful or not needed, False otherwise
        """
        if not self._google_drive_client:
            return True  # Not using Drive, so "success"

        try:
            new_token = await self._google_drive_client.async_refresh_token()
            
            if new_token:
                _LOGGER.info("Google Drive token refreshed successfully")
                # Update config entry with new token
                # This should be handled by config flow, but we log it here
                return True
            
            return False

        except Exception as err:
            _LOGGER.error(f"Error refreshing Google Drive token: {err}", exc_info=True)
            return False
            
            
