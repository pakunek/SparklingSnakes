import os
from typing import Any, Optional

import toml
from sparkling_snakes import consts


class AppConfigHelper(object):
    """Configuration management class."""

    _instance: Optional['AppConfigHelper'] = None
    _config: Optional[dict[str, Any]] = None

    def __new__(cls) -> 'AppConfigHelper':
        """Ensure Singleton properties."""
        if cls._instance is None:
            cls._instance = super(AppConfigHelper, cls).__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls) -> None:
        """Load config from known paths.

        The priority of paths is as follows:
        * <consts.DEFAULT_CONFIG_PATH>/consts.DEFAULT_CONFIG_NAME
        * ./consts.DEFAULT_CONFIG_NAME

        :return: None
        """
        if os.path.isfile(config_path:= os.path.join(consts.DEFAULT_CONFIG_PATH, consts.DEFAULT_CONFIG_NAME)):
            print(f"Loading configuration file from path: {config_path}")
            cls._instance._config = toml.load(config_path)
        else:
            print(f"No user-defined config found in {config_path}, "
                  f"falling back to defaults (./{consts.DEFAULT_CONFIG_NAME})")
            cls._instance._config = toml.load(os.path.relpath(consts.DEFAULT_CONFIG_NAME))

    @classmethod
    def get_config(cls) -> dict[str, Any]:
        """Return the preloaded configuration.

        :return: dict containing configuration values
        """
        if not cls._instance._config:
            cls._load_config()
        return cls._instance._config
