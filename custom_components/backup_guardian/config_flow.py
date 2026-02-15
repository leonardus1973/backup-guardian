"""Config flow for Backup Guardian integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_GOOGLE_DRIVE_ENABLED,
    CONF_GOOGLE_CLIENT_ID,
    CONF_GOOGLE_CLIENT_SECRET,
    CONF_GOOGLE_FOLDER_ID,
    CONF_GOOGLE_TOKEN,
)
from .oauth_handler import (
    GoogleDriveOAuth2Handler,
    async_validate_credentials,
    extract_folder_id_from_url,
)

_LOGGER = logging.getLogger(__name__)


class BackupGuardianConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Backup Guardian."""

    VERSION = 1

    def __init__(self):
        """Initialize config flow."""
        self._google_drive_data = {}
        self._oauth_handler = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            # Create entry with basic config
            return self.async_create_entry(
                title="Backup Guardian",
                data={
                    CONF_GOOGLE_DRIVE_ENABLED: False,
                },
            )

        # Show form to user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "docs_url": "https://github.com/leonardus1973/backup-guardian"
            },
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BackupGuardianOptionsFlow(config_entry)


class BackupGuardianOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Backup Guardian."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._google_drive_data = {}
        self._oauth_handler = None

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_menu()

    async def async_step_menu(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show configuration menu."""
        return self.async_show_menu(
            step_id="menu",
            menu_options=["google_drive", "advanced"],
        )

    async def async_step_google_drive(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure Google Drive integration."""
        errors = {}

        # Get current config
        current_enabled = self.config_entry.data.get(CONF_GOOGLE_DRIVE_ENABLED, False)

        if user_input is not None:
            if not user_input.get("enable_google_drive"):
                # User wants to disable Google Drive
                new_data = {**self.config_entry.data}
                new_data[CONF_GOOGLE_DRIVE_ENABLED] = False
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=new_data
                )
                return self.async_create_entry(title="", data={})

            # User wants to enable - proceed to credentials
            return await self.async_step_google_credentials()

        # Show enable/disable form
        return self.async_show_form(
            step_id="google_drive",
            data_schema=vol.Schema(
                {
                    vol.Required("enable_google_drive", default=current_enabled): bool,
                }
            ),
            description_placeholders={
                "status": "Abilitato" if current_enabled else "Disabilitato",
                "setup_guide": "Vedi GOOGLE_DRIVE_SETUP.md per la guida completa",
            },
        )

    async def async_step_google_credentials(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure Google Drive OAuth credentials."""
        errors = {}

        if user_input is not None:
            client_id = user_input[CONF_GOOGLE_CLIENT_ID]
            client_secret = user_input[CONF_GOOGLE_CLIENT_SECRET]
            folder_input = user_input.get(CONF_GOOGLE_FOLDER_ID, "root")

            # Validate credentials format
            if not await async_validate_credentials(
                self.hass, client_id, client_secret
            ):
                errors["base"] = "invalid_credentials"
            else:
                # Extract folder ID from URL if needed
                folder_id = extract_folder_id_from_url(folder_input)
                if not folder_id:
                    errors["folder_id"] = "invalid_folder_id"
                else:
                    # Store credentials and proceed to OAuth
                    self._google_drive_data = {
                        CONF_GOOGLE_CLIENT_ID: client_id,
                        CONF_GOOGLE_CLIENT_SECRET: client_secret,
                        CONF_GOOGLE_FOLDER_ID: folder_id,
                    }
                    return await self.async_step_google_oauth()

        # Get current values if any
        current_client_id = self.config_entry.data.get(CONF_GOOGLE_CLIENT_ID, "")
        current_folder_id = self.config_entry.data.get(CONF_GOOGLE_FOLDER_ID, "root")

        return self.async_show_form(
            step_id="google_credentials",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_GOOGLE_CLIENT_ID, default=current_client_id
                    ): str,
                    vol.Required(CONF_GOOGLE_CLIENT_SECRET): str,
                    vol.Optional(
                        CONF_GOOGLE_FOLDER_ID, default=current_folder_id
                    ): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "setup_guide": "Segui GOOGLE_DRIVE_SETUP.md per ottenere Client ID e Secret",
                "folder_help": "Inserisci l'URL della cartella o l'ID diretto. Usa 'root' per la cartella principale.",
            },
        )

    async def async_step_google_oauth(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle Google OAuth authorization."""
        errors = {}

        # Initialize OAuth handler if not done
        if not self._oauth_handler:
            self._oauth_handler = GoogleDriveOAuth2Handler(
                self.hass,
                self._google_drive_data[CONF_GOOGLE_CLIENT_ID],
                self._google_drive_data[CONF_GOOGLE_CLIENT_SECRET],
            )

        if user_input is not None:
            authorization_code = user_input.get("authorization_code", "").strip()

            if not authorization_code:
                errors["authorization_code"] = "code_required"
            else:
                # Exchange code for tokens
                tokens = await self._oauth_handler.async_get_tokens(authorization_code)

                if not tokens:
                    errors["base"] = "auth_failed"
                    _LOGGER.error("Failed to exchange authorization code for tokens")
                else:
                    # Success! Store everything
                    new_data = {**self.config_entry.data}
                    new_data.update(
                        {
                            CONF_GOOGLE_DRIVE_ENABLED: True,
                            CONF_GOOGLE_CLIENT_ID: self._google_drive_data[
                                CONF_GOOGLE_CLIENT_ID
                            ],
                            CONF_GOOGLE_CLIENT_SECRET: self._google_drive_data[
                                CONF_GOOGLE_CLIENT_SECRET
                            ],
                            CONF_GOOGLE_FOLDER_ID: self._google_drive_data[
                                CONF_GOOGLE_FOLDER_ID
                            ],
                            CONF_GOOGLE_TOKEN: {
                                "access_token": tokens.get("access_token"),
                                "refresh_token": tokens.get("refresh_token"),
                                "token_type": tokens.get("token_type"),
                            },
                        }
                    )

                    self.hass.config_entries.async_update_entry(
                        self.config_entry, data=new_data
                    )

                    _LOGGER.info("Google Drive integration configured successfully")

                    return self.async_create_entry(
                        title="",
                        data={},
                    )

        # Generate authorization URL
        auth_url = self._oauth_handler.get_authorization_url()

        return self.async_show_form(
            step_id="google_oauth",
            data_schema=vol.Schema(
                {
                    vol.Required("authorization_code"): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "auth_url": auth_url,
                "instructions": (
                    "1. Clicca sul link qui sopra\n"
                    "2. Accedi con il tuo account Google\n"
                    "3. Autorizza l'accesso a Google Drive\n"
                    "4. Copia il codice che Google ti mostra\n"
                    "5. Incolla il codice qui sotto"
                ),
            },
        )

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure advanced settings."""
        # Placeholder for future advanced settings
        return self.async_show_form(
            step_id="advanced",
            data_schema=vol.Schema({}),
            description_placeholders={
                "info": "Impostazioni avanzate disponibili nelle prossime versioni"
            },
        )
