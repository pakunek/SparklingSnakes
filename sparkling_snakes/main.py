from fastapi import FastAPI

from sparkling_snakes.api.routes.api import router
from sparkling_snakes.consts import API_PREFIX
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.app_logging import AppLoggingHelper


def get_application() -> FastAPI:
    config_helper: AppConfigHelper = AppConfigHelper()
    AppLoggingHelper.configure_logging(config_helper.get_config())

    application: FastAPI = FastAPI(docs_url="/docs")
    application.include_router(router, prefix=API_PREFIX)
    return application


app: FastAPI = get_application()
