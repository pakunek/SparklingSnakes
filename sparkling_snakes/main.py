from fastapi import FastAPI
from sparkling_snakes.api import models
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper

config_helper = AppConfigHelper()
config_helper.configure_logging()
pyspark_helper = PySparkHelper(config_helper)
pyspark_helper.connect_to_cluster()

app = FastAPI(docs_url="/docs")


@app.post("/processor/tasks/")
async def post_processor_task(task: models.NewTask) -> dict[str, str]:
    """POST method for /processor/tasks/ endpoint.

    :param task: NewTask class instance
    :return: simple message with input presentation (temporary)
    :raises: HTTPException with 400 status code if the Task is invalid
    """
    task.validate_data()
    return {"message": f"Calculations complete, primes for given range are: "
                       f"{pyspark_helper.test_cluster_operation_primes_from_range(task.n)}"}
