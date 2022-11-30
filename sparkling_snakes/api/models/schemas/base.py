from abc import ABC, abstractmethod


class Verifiable(ABC):
    @abstractmethod
    def validate_data(self) -> None:
        """Validate if object consists of proper data.

        :return: None
        :raises: HTTPException with 400 status code if object is invalid
        """
