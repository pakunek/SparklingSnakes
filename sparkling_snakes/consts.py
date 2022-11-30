import os

MINIMUM_PROCESSOR_TASKS_ALLOWED: int = 2

DEFAULT_CONFIG_PATH: str = os.path.join("/etc", "opt")
DEFAULT_CONFIG_NAME: str = "sparkling_snakes.toml"

LOGGING_MAIN_FORMAT: str = "%(asctime)s %(message)s"
LOGGING_DATE_FORMAT: str = "%m/%d/%Y %I:%M:%S %p"

API_PREFIX: str = "/processor"
