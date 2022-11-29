import os

import toml
from sparkling_snakes import consts
import logging


class AppConfigHelper(object):  # TODO: Cleanup, docs
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfigHelper, cls).__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def get_config(cls):
        return cls._instance.config

    @classmethod
    def configure_logging(cls):
        logging.basicConfig(format=consts.LOGGING_MAIN_FORMAT, datefmt=consts.LOGGING_DATE_FORMAT)
        logging.info("Logging has been configured properly")

    @classmethod
    def _load_config(cls):
        config_path = os.path.join(consts.DEFAULT_CONFIG_PATH, consts.DEFAULT_CONFIG_NAME)

        if os.path.isfile(config_path):
            print(f"Loading config from the following path: {config_path}")
            cls._instance.config = toml.load(config_path)
        else:
            print(f"No user-defined config found in {config_path}, falling back to defaults")
            cls._instance.config = toml.load(os.path.relpath(consts.DEFAULT_CONFIG_NAME))
