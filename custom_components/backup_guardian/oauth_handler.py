"""OAuth2 handler for Google Drive authentication.

This module handles the OAuth2 flow for Google Drive integration.
"""
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .const import (
    GOOGLE_DRIVE_API_SCOPES,
    OAUTH_AUTH_URL,
    OAUTH_TOKEN_URL,
)

_LOGGER = logging.getLogger(__name__)


class GoogleDriveOAuth2Handler:
    """Handle OAuth2 flow for Google Drive."""

    def __init__(self, hass: HomeAssistant, client_id: str, client_secret: str) -> None:
        """Initialize OAuth2 handler.
        
        Args:
            hass: Home Assistant instance
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret
        """
        self.hass = hass
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str | None = None) -> str:
        """Generate Google OAuth authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL for user to visit
        """
        from urllib.parse import urlencode

        params = {
            "client_id": self.client_id,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",  # For manual code entry
            "response_type": "code",
            "scope": " ".join(GOOGLE_DRIVE_API_SCOPES),
            "access_type": "offline",  # Request refresh token
            "prompt": "consent",  # Force consent screen to get refresh token
        }
        
        if state:
            params["state"] = state

        return f"{OAUTH_AUTH_URL}?{urlencode(params)}"

    async def async_get_tokens(self, authorization_code: str) -> dict[str, Any] | None:
        """Exchange authorization code for tokens.
        
        Args:
            authorization_code: Code from Google OAuth authorization
            
        Returns:
            Dict with 'access_token', 'refresh_token', 'expiry' or None if failed
        """
        try:
            import aiohttp
            from urllib.parse import urlencode

            data = {
                "code": authorization_code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
                "grant_type": "authorization_code",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    OAUTH_TOKEN_URL,
                    data=urlencode(data),
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        _LOGGER.error(f"Token exchange failed: {error_text}")
                        return None

                    result = await response.json()
                    
                    return {
                        "access_token": result.get("access_token"),
                        "refresh_token": result.get("refresh_token"),
                        "token_type": result.get("token_type"),
                        "expires_in": result.get("expires_in"),
                    }

        except Exception as err:
            _LOGGER.error(f"Error exchanging authorization code: {err}", exc_info=True)
            return None

    async def async_refresh_token(self, refresh_token: str) -> dict[str, Any] | None:
        """Refresh access token using refresh token.
        
        Args:
            refresh_token: Google OAuth refresh token
            
        Returns:
            Dict with new 'access_token' or None if failed
        """
        try:
            import aiohttp
            from urllib.parse import urlencode

            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    OAUTH_TOKEN_URL,
                    data=urlencode(data),
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        _LOGGER.error(f"Token refresh failed: {error_text}")
                        return None

                    result = await response.json()
                    
                    return {
                        "access_token": result.get("access_token"),
                        "expires_in": result.get("expires_in"),
                    }

        except Exception as err:
            _LOGGER.error(f"Error refreshing token: {err}", exc_info=True)
            return None


async def async_validate_credentials(
    hass: HomeAssistant, client_id: str, client_secret: str
) -> bool:
    """Validate Google OAuth credentials format.
    
    Args:
        hass: Home Assistant instance
        client_id: Google OAuth client ID
        client_secret: Google OAuth client secret
        
    Returns:
        True if credentials appear valid (basic format check)
    """
    # Basic validation: check format
    if not client_id or not client_secret:
        return False
    
    # Client ID should end with .apps.googleusercontent.com
    if not client_id.endswith(".apps.googleusercontent.com"):
        _LOGGER.warning("Client ID doesn't match expected format")
        return False
    
    # Client secret should be alphanumeric with some symbols
    if len(client_secret) < 20:
        _LOGGER.warning("Client secret appears too short")
        return False
    
    return True


def extract_folder_id_from_url(url: str) -> str | None:
    """Extract folder ID from Google Drive URL.
    
    Supports:
    - https://drive.google.com/drive/folders/FOLDER_ID
    - https://drive.google.com/drive/u/0/folders/FOLDER_ID
    
    Args:
        url: Google Drive folder URL or folder ID
        
    Returns:
        Folder ID or None if can't parse
    """
    import re
    
    # If it's already just an ID (no URL), return it
    if not url.startswith("http"):
        return url
    
    # Try to extract from URL
    match = re.search(r"/folders/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    
    _LOGGER.warning(f"Could not extract folder ID from: {url}")
    return None
    
