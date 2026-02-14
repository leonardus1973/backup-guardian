"""Constants for the Backup Guardian integration."""

DOMAIN = "backup_guardian"

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
ATTR_BACKUP_DESTINATION = "backup_destination"  # NEW: Destinazione backup (local, google_drive, dropbox, ecc.)

