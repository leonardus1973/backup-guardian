"""Google Drive integration for Backup Guardian.

This module handles communication with Google Drive API to fetch backup files.
"""
import logging
import re
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import (
    BACKUP_FILE_PATTERNS,
    DESTINATION_GOOGLE_DRIVE,
    GOOGLE_DRIVE_API_SCOPES,
    GOOGLE_DRIVE_API_VERSION,
)

_LOGGER = logging.getLogger(__name__)


class GoogleDriveClient:
    """Google Drive API client for backup scanning."""

    def __init__(self, hass: HomeAssistant, credentials: dict) -> None:
        """Initialize Google Drive client.
        
        Args:
            hass: Home Assistant instance
            credentials: Dict with 'client_id', 'client_secret', 'token', 'folder_id'
        """
        self.hass = hass
        self._credentials = credentials
        self._service = None

    async def async_setup(self) -> bool:
        """Setup Google Drive API service.
        
        Returns:
            True if setup successful, False otherwise
        """
        try:
            # Import Google API client (will be installed via requirements)
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials

            # Create credentials object from token
            creds = Credentials(
                token=self._credentials.get("token"),
                refresh_token=self._credentials.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self._credentials.get("client_id"),
                client_secret=self._credentials.get("client_secret"),
                scopes=GOOGLE_DRIVE_API_SCOPES,
            )

            # Build service
            self._service = build("drive", GOOGLE_DRIVE_API_VERSION, credentials=creds)
            
            _LOGGER.info("Google Drive API service initialized successfully")
            return True

        except ImportError:
            _LOGGER.error(
                "Google API client not installed. "
                "Add 'google-api-python-client>=2.0.0' to requirements"
            )
            return False
        except Exception as err:
            _LOGGER.error(f"Failed to setup Google Drive service: {err}", exc_info=True)
            return False

    async def async_get_backups(self) -> list[dict[str, Any]]:
        """Fetch backup files from Google Drive.
        
        Returns:
            List of backup file dictionaries with metadata
        """
        if not self._service:
            _LOGGER.error("Google Drive service not initialized")
            return []

        try:
            folder_id = self._credentials.get("folder_id", "root")
            
            # Query for backup files in specified folder
            # Build query to match backup patterns
            query_parts = []
            for pattern in BACKUP_FILE_PATTERNS:
                # Convert regex to simple name contains (Drive doesn't support full regex)
                if ".tar.gz" in pattern:
                    query_parts.append("name contains '.tar.gz'")
                elif ".tar" in pattern:
                    query_parts.append("name contains '.tar'")
                elif ".tgz" in pattern:
                    query_parts.append("name contains '.tgz'")
            
            query = f"'{folder_id}' in parents and ({' or '.join(query_parts)}) and trashed=false"
            
            _LOGGER.debug(f"Google Drive query: {query}")
            
            # Execute query
            results = await self.hass.async_add_executor_job(
                self._fetch_files, query
            )
            
            if not results:
                _LOGGER.info("No backup files found in Google Drive")
                return []
            
            # Process results
            backups = []
            for item in results.get("files", []):
                backup_info = self._process_drive_file(item)
                if backup_info:
                    backups.append(backup_info)
            
            _LOGGER.info(f"Found {len(backups)} backup files on Google Drive")
            return backups

        except Exception as err:
            _LOGGER.error(f"Error fetching backups from Google Drive: {err}", exc_info=True)
            return []

    def _fetch_files(self, query: str) -> dict:
        """Fetch files from Drive (blocking call for executor).
        
        Args:
            query: Drive API query string
            
        Returns:
            API response dict
        """
        return (
            self._service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id, name, size, createdTime, modifiedTime, md5Checksum)",
                pageSize=100,
            )
            .execute()
        )

    def _process_drive_file(self, file_data: dict) -> dict[str, Any] | None:
        """Process a Google Drive file into backup format.
        
        Args:
            file_data: Raw file data from Google Drive API
            
        Returns:
            Processed backup dict or None if invalid
        """
        try:
            # Validate file matches backup pattern
            filename = file_data.get("name", "")
            if not self._is_backup_file(filename):
                return None

            # Extract date from filename or use modified time
            date_obj = self._extract_date_from_filename(filename)
            if not date_obj:
                # Fallback to file's modified time
                modified_time = file_data.get("modifiedTime")
                if modified_time:
                    date_obj = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))
                    date_obj = dt_util.as_local(date_obj)
                else:
                    date_obj = dt_util.now()

            # Calculate size
            size_bytes = int(file_data.get("size", 0))
            size_mb = round(size_bytes / (1024 * 1024), 2)

            # Use MD5 as hash (Google Drive provides it)
            file_hash = file_data.get("md5Checksum", file_data.get("id", ""))

            return {
                "name": filename,
                "slug": file_data.get("id"),  # Use Drive file ID as slug
                "size": size_bytes,
                "size_mb": size_mb,
                "date": date_obj.strftime("%Y-%m-%d"),
                "time": date_obj.strftime("%H:%M:%S"),
                "datetime": date_obj,
                "hash": file_hash,
                "type": "full",  # Assume full backup
                "protected": False,
                "compressed": filename.endswith((".gz", ".tgz")),
                "destination": DESTINATION_GOOGLE_DRIVE,
                "destination_name": "Google Drive",
                "drive_file_id": file_data.get("id"),
            }

        except Exception as err:
            _LOGGER.error(f"Error processing Drive file: {err}", exc_info=True)
            return None

    def _is_backup_file(self, filename: str) -> bool:
        """Check if filename matches backup patterns.
        
        Args:
            filename: File name to check
            
        Returns:
            True if matches backup pattern
        """
        for pattern in BACKUP_FILE_PATTERNS:
            if re.match(pattern, filename):
                return True
        return False

    def _extract_date_from_filename(self, filename: str) -> datetime | None:
        """Try to extract date from backup filename.
        
        Common patterns:
        - backup_2026-02-15_17-16-00.tar
        - Full backup 2026-02-15 17:16:00.tar
        
        Args:
            filename: Backup filename
            
        Returns:
            Datetime object or None if can't parse
        """
        try:
            # Pattern 1: YYYY-MM-DD HH:MM:SS
            import re
            pattern = r"(\d{4}-\d{2}-\d{2})[_ ](\d{2})[:-](\d{2})[:-](\d{2})"
            match = re.search(pattern, filename)
            if match:
                date_str = f"{match.group(1)} {match.group(2)}:{match.group(3)}:{match.group(4)}"
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                # Assume UTC, convert to local
                date_obj = date_obj.replace(tzinfo=dt_util.UTC)
                return dt_util.as_local(date_obj)
            
            # Pattern 2: YYYY-MM-DD only
            pattern = r"(\d{4}-\d{2}-\d{2})"
            match = re.search(pattern, filename)
            if match:
                date_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
                date_obj = date_obj.replace(tzinfo=dt_util.UTC)
                return dt_util.as_local(date_obj)

        except Exception as err:
            _LOGGER.debug(f"Could not extract date from filename {filename}: {err}")
        
        return None

    async def async_refresh_token(self) -> dict | None:
        """Refresh OAuth token if expired.
        
        Returns:
            New token dict or None if refresh failed
        """
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request

            creds = Credentials(
                token=self._credentials.get("token"),
                refresh_token=self._credentials.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self._credentials.get("client_id"),
                client_secret=self._credentials.get("client_secret"),
                scopes=GOOGLE_DRIVE_API_SCOPES,
            )

            if creds.expired and creds.refresh_token:
                await self.hass.async_add_executor_job(creds.refresh, Request())
                
                return {
                    "token": creds.token,
                    "refresh_token": creds.refresh_token,
                    "expiry": creds.expiry.isoformat() if creds.expiry else None,
                }

        except Exception as err:
            _LOGGER.error(f"Failed to refresh token: {err}", exc_info=True)
        
        return None
        
