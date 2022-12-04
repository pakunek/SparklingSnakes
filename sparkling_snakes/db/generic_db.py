from abc import ABC, abstractmethod
from typing import Any

from sparkling_snakes.processor.data_models import FileMetadata


# TODO: Docs?
class GenericDatabase(ABC):
    @abstractmethod
    def init_connection(self, config: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def metadata_exists_by_id(self, object_id: str) -> bool:
        pass

    @abstractmethod
    def put_metadata(self, metadata_object: FileMetadata) -> None:
        pass

    @abstractmethod
    def _map_file_metadata_to_db_object(self, metadata_object: FileMetadata) -> Any:
        pass
