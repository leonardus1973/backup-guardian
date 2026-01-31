"""Constants for Backup Guardian integration."""

DOMAIN = "backup_guardian"
PLATFORMS = ["sensor"]

# Percorsi dei backup
BACKUP_PATH = "/backup"

# Intervallo di aggiornamento (in secondi)
UPDATE_INTERVAL = 300  # 5 minuti

# Attributi dei sensori
ATTR_BACKUP_NAME = "backup_name"
ATTR_BACKUP_DATE = "backup_date"
ATTR_BACKUP_TIME = "backup_time"
ATTR_BACKUP_SIZE = "backup_size"
ATTR_BACKUP_HASH = "backup_hash"
ATTR_BACKUP_TYPE = "backup_type"
ATTR_BACKUP_PROTECTED = "protected"
ATTR_BACKUP_COMPRESSED = "compressed"
ATTR_BACKUP_LIST = "backup_list"
