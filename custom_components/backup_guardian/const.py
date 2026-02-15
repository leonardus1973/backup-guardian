"""Constants for the Backup Guardian integration."""

DOMAIN = "backup_guardian"

# Platforms
PLATFORMS = ["sensor"]

# Update interval in seconds (5 minutes)
UPDATE_INTERVAL = 300

# Sensor attributes
ATTR_BACKUP_NAME = "backup_name"
ATTR_BACKUP_DATE = "backup_date"
ATTR_BACKUP_TIME = "backup_time"
ATTR_BACKUP_SIZE = "backup_size"
ATTR_BACKUP_HASH = "backup_hash"
ATTR_BACKUP_TYPE = "backup_type"
ATTR_BACKUP_SLUG = "backup_slug"
ATTR_BACKUP_LIST = "backup_list"
ATTR_BACKUP_DESTINATION = "backup_destination"

# Backup destinations
DESTINATION_LOCAL = "local"
DESTINATION_GOOGLE_DRIVE = "google_drive"
DESTINATION_DROPBOX = "dropbox"
DESTINATION_ONEDRIVE = "onedrive"

# Destination friendly names
DESTINATION_NAMES = {
    DESTINATION_LOCAL: "Home Assistant Locale",
    DESTINATION_GOOGLE_DRIVE: "Google Drive",
    DESTINATION_DROPBOX: "Dropbox",
    DESTINATION_ONEDRIVE: "OneDrive",
}

# Google Drive configuration
CONF_GOOGLE_DRIVE_ENABLED = "google_drive_enabled"
CONF_GOOGLE_CLIENT_ID = "google_client_id"
CONF_GOOGLE_CLIENT_SECRET = "google_client_secret"
CONF_GOOGLE_FOLDER_ID = "google_folder_id"
CONF_GOOGLE_TOKEN = "google_token"

# Google Drive API
GOOGLE_DRIVE_API_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
GOOGLE_DRIVE_API_VERSION = "v3"

# Backup file patterns (regex)
BACKUP_FILE_PATTERNS = [
    r".*\.tar$",      # .tar files
    r".*\.tar\.gz$",  # .tar.gz files
    r".*\.tgz$",      # .tgz files
]

# OAuth2
OAUTH_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"  # For manual code entry
OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

