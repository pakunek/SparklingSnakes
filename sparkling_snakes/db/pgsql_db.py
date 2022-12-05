import logging
from typing import Any

import sqlalchemy.engine
from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from sparkling_snakes.db.generic_db import GenericDatabase
from sparkling_snakes.db.models.pgsql.metadata import Metadata
from sparkling_snakes.exceptions import DBConnectionNotInitialized
from sparkling_snakes.processor.data_models import FileMetadata
from sparkling_snakes.processor.types import Config

log = logging.getLogger(__name__)


class PostgreSQLDatabase(GenericDatabase):
    """PostgreSQL-specific DB operations class."""

    _engine: sqlalchemy.engine.Engine = None

    def init_connection(self, config: Config) -> None:
        if not self._engine:
            self._engine = create_engine(config['db']['conn_string'])

    def _get_session(self) -> orm.Session:
        """Create and return session.

        :return:SQLAlchemy Session object
        """
        if not self._engine:
            raise DBConnectionNotInitialized
        return sessionmaker(bind=self._engine)()

    def metadata_exists_by_id(self, object_id: str) -> bool:
        try:
            with self._get_session() as session:
                return session.query(Metadata.id).filter_by(id=object_id).first() is not None
        except NoResultFound:
            return False
        except SQLAlchemyError:
            log.exception("Unknown error while checking %s object existence", object_id)
            raise

    def put_metadata(self, object_id: str, metadata_object: FileMetadata) -> bool:
        try:
            with self._get_session() as session:
                db_object = self._map_file_metadata_to_db_object(object_id, metadata_object)
                session.add(db_object)
                session.commit()
                log.debug("Object %s %s added to DB", object_id, metadata_object)
                return True
        except SQLAlchemyError:
            log.exception("Unknown error while adding %s object to DB", object_id)
            return False

    def _map_file_metadata_to_db_object(self, object_id: str, metadata_object: FileMetadata) -> Any:
        return Metadata(id=object_id,
                        imports=metadata_object.imports,
                        exports=metadata_object.exports,
                        path=metadata_object.path,
                        size=metadata_object.size,
                        type=metadata_object.type,
                        arch=metadata_object.arch)
