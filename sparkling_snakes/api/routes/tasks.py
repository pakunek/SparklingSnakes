from fastapi import APIRouter
from starlette import status

from sparkling_snakes.api.models.schemas.tasks import TaskInCreate, TaskInResponse
from sparkling_snakes.services.tasks import TasksService

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskInResponse,
             name="tasks:run-new-task")
async def post_processor_task(task: TaskInCreate) -> TaskInResponse:
    """POST method for /processor/tasks/ endpoint.

    :param task: NewTask class instance
    :return: simple message with input presentation (temporary)
    :raises: HTTPException with 400 status code if the Task is invalid
    """
    task.validate_data()
    return TasksService.run_task(task.n)
