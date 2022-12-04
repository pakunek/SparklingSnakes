import logging

from sparkling_snakes import consts
from sparkling_snakes.processor.types import Config


class AppLoggingHelper:
    """Logging management class."""

    level_mapper: dict[str, int] = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    @staticmethod
    def configure_logging(config: Config) -> None:
        """Configure logging using project consts.

        :return: None
        """
        config_level: str = config.get('project', {}).get('logging_level', 'INFO')

        logging.basicConfig(format=consts.LOGGING_MAIN_FORMAT, datefmt=consts.LOGGING_DATE_FORMAT,
                            level=AppLoggingHelper.level_mapper[config_level])
