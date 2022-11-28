from fastapi import FastAPI
from sparkling_snakes.api import models

app = FastAPI(docs_url="/docs")


@app.post("/processor/tasks/")
async def post_processor_task(task: models.NewTask) -> dict[str, str]:
    """POST method for /processor/tasks/ endpoint.

    :param task: NewTask class instance
    :return: simple message with input presentation (temporary)
    :raises: HTTPException with 400 status code if the Task is invalid
    """
    task.validate_data()
    return {"message": f"You have proposed the following URL for Task Processing: {task.URL}"}
