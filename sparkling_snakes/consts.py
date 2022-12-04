import os

MINIMUM_PROCESSOR_TASKS_ALLOWED: int = 2

DEFAULT_CONFIG_PATH: str = os.path.join("/etc", "opt")
DEFAULT_CONFIG_NAME: str = "sparkling_snakes.toml"

LOGGING_MAIN_FORMAT: str = "%(asctime)s %(message)s"
LOGGING_DATE_FORMAT: str = "%m/%d/%Y %I:%M:%S %p"

API_PREFIX: str = "/processor"
FILE_STORAGE: str = "/tmp/s3-files"

DEFAULT_DB_INT_VALUE: int = -1
DEFAULT_DB_STR_VALUE: str = "<N/A>"

EXIFTOOL_ARCHITECTURE_MAPPING: dict[str, str] = {
    'AMD AMD64': 'x64',
    'Intel 386 or later, and compatibles': 'x86'
}
EXIFTOOL_FILE_SIZE_FIELD: str = 'FileSize'
EXIFTOOL_FILE_TYPE_FIELD: str = 'FileTypeExtension'
EXIFTOOL_ARCHITECTURE_FIELD: str = 'MachineType'
