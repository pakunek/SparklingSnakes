from fastapi import HTTPException
from pydantic import BaseModel

from sparkling_snakes import consts
from sparkling_snakes.api.models.schemas.base import Verifiable


class TaskInCreate(BaseModel, Verifiable):
    region_name: str
    bucket_name: str
    n: int

    def validate_data(self) -> None:
        if not self.bucket_name or not self.bucket_name or \
                not self.n or self.n < consts.MINIMUM_PROCESSOR_TASKS_ALLOWED:
            raise HTTPException(status_code=400, detail="No Task or Task with improper value(s) has been provided")


class TaskInResponse(BaseModel):
    message: str
