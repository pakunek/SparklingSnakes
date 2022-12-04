from abc import ABC, abstractmethod
from typing import Any

from sparkling_snakes.processor.data_models import FileMetadata
from sparkling_snakes.processor.types import Config


class GenericDatabase(ABC):
    """Abstract DB operations class."""

    @abstractmethod
    def init_connection(self, config: Config) -> None:
        """Initialize DB connection.

        :param config: project configuration dict
        """

    @abstractmethod
    def metadata_exists_by_id(self, object_id: str) -> bool:
        """Notify if Metadata with given ID exists.

        :param object_id: unique ID of an object for indexing/PK purpose
        """

    @abstractmethod
    def put_metadata(self, object_id: str, metadata_object: FileMetadata) -> None:
        """Transform and store Metadata obj in DB.

        :param object_id: unique ID of an object for indexing/PK purpose
        :param metadata_object: dataclass containing metadata properties
        """

    @abstractmethod
    def _map_file_metadata_to_db_object(self, object_id: str, metadata_object: FileMetadata) -> Any:
        """Map FileMetadata to DB object.

        Method created in order to enforce separation of mapping logic.

        :param object_id: unique ID of an object for indexing/PK purpose
        :param metadata_object: dataclass containing metadata properties
        :return: DB-specific object ready to be stored
        """
