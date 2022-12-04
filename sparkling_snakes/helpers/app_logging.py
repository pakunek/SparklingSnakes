import logging
from typing import Any

from sparkling_snakes import consts


class AppLoggingHelper(object):
    """Logging management class."""

    level_mapper: dict[str, int] = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    @staticmethod
    def configure_logging(config: dict[str, Any]) -> None:
        """Configure logging using project consts.

        :return: None
        """
        config_level: str = config.get('project', {}).get('logging_level', 'INFO')

        logging.basicConfig(format=consts.LOGGING_MAIN_FORMAT, datefmt=consts.LOGGING_DATE_FORMAT,
                            level=AppLoggingHelper.level_mapper[config_level])
