from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from sparkling_snakes.db.generic_db import GenericDatabase
from sparkling_snakes.db.models.pgsql.metadata import Metadata
from sparkling_snakes.exceptions import DBConnectionNotInitialized
from sparkling_snakes.processor.data_models import FileMetadata
import logging

log = logging.getLogger(__name__)


# TODO: Cleanup, docs
class PostgreSQLDatabase(GenericDatabase):

    _engine = None

    def init_connection(self, config: dict[str, Any]) -> None:
        if not self._engine:
            self._engine = create_engine(config['db']['conn_string'])

    def _get_session(self):
        if not self._engine:
            raise DBConnectionNotInitialized
        return sessionmaker(bind=self._engine)()

    def metadata_exists_by_id(self, object_id: str) -> bool:
        exists: bool = False
        try:
            session = self._get_session()
            exists = session.query(Metadata.id).filter_by(id=object_id).first() is not None
            session.close()
        except NoResultFound:
            return exists
        except SQLAlchemyError:
            log.exception("Unknown error while checking %s object existence", object_id)
        log.info("Object %s %s in DB", object_id, "exists" if exists else "does not exist")
        return exists

    def put_metadata(self, metadata_object: FileMetadata) -> None:
        pass

    def _map_file_metadata_to_db_object(self, metadata_object: FileMetadata) -> Any:
        pass
