import logging

from fastapi import FastAPI

from sparkling_snakes import consts
from sparkling_snakes.api.routes.api import router
from sparkling_snakes.consts import API_PREFIX
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.app_logging import AppLoggingHelper
from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper

log = logging.getLogger(__name__)


def get_application() -> FastAPI:
    config_helper: AppConfigHelper = AppConfigHelper()
    AppLoggingHelper.configure_logging(config := config_helper.get_config())
    FilesystemOperationsHelper.create_directory(consts.FILE_STORAGE)
    PySparkHelper(config)

    application: FastAPI = FastAPI(docs_url="/docs")
    application.include_router(router, prefix=API_PREFIX)
    log.info("Application initialized properly")
    return application


app: FastAPI = get_application()
