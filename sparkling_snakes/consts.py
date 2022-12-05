import os
from enum import Enum

S3_PAGE_SIZE: int = 100
EXPECTED_S3_PREFIXES: list[str] = ['0', '1']
UNSUPPORTED_S3_KEY_EXTENSIONS: list[str] = ['html']

DEFAULT_CONFIG_PATH: str = os.path.join("/etc", "opt")
DEFAULT_CONFIG_NAME: str = "sparkling_snakes.toml"

LOGGING_MAIN_FORMAT: str = "%(asctime)s %(message)s"
LOGGING_DATE_FORMAT: str = "%m/%d/%Y %I:%M:%S %p"

API_PREFIX: str = "/processor"
FILE_STORAGE: str = "/s3-files"

DEFAULT_DB_INT_VALUE: int = -1
DEFAULT_DB_STR_VALUE: str = "<N/A>"

EXPECTED_OPERATIONS_PER_FILE: int = 5

EXIFTOOL_ARCHITECTURE_MAPPING: dict[str, str] = {
    'AMD AMD64': 'x64',
    'Intel 386 or later, and compatibles': 'x86'
}


class ExiftoolSupportedFields(Enum):
    file_size = 'FileSize'
    file_type = 'FileTypeExtension'
    architecture = 'MachineType'
