from fastapi import APIRouter

from sparkling_snakes.api.routes import tasks

router = APIRouter()
router.include_router(tasks.router, prefix="/tasks")
