from fastapi import HTTPException
from pydantic import BaseModel
import math
from sparkling_snakes import consts
from sparkling_snakes.api.models.schemas.base import Verifiable


class TaskInCreate(BaseModel, Verifiable):
    region_name: str
    bucket_name: str
    files_total: int

    def validate_data(self) -> None:
        if not self.bucket_name or not self.bucket_name or \
                not self.files_total or math.floor(self.files_total / len(consts.EXPECTED_S3_PREFIXES)) < 1:
            raise HTTPException(status_code=400, detail="No Task or Task with improper value(s) has been provided")


class TaskInResponse(BaseModel):
    message: str
