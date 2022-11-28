from fastapi import HTTPException
from pydantic import BaseModel
from abc import ABC, abstractmethod


class Verifiable(ABC):
    @abstractmethod
    def validate_data(self) -> None:
        """Validate if object consists of proper data.

        :return: None
        :raises: HTTPException with 400 status code if object is invalid
        """


class NewTask(BaseModel, Verifiable):
    URL: str

    def validate_data(self) -> None:
        if not self.URL:
            raise HTTPException(status_code=400,
                                detail="No Task or Task with improper value(s) has been provided")
