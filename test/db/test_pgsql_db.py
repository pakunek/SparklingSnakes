import unittest
from unittest import mock

from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from sparkling_snakes.db.pgsql_db import PostgreSQLDatabase
from sparkling_snakes.exceptions import DBConnectionNotInitialized


class TestPostgreSQLDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db_client = PostgreSQLDatabase()

    def tearDown(self) -> None:
        self.db_client = None

    def test__get_session_exception_without_initialization(self):
        with self.assertRaises(DBConnectionNotInitialized):
            self.db_client._get_session()

    @mock.patch('sparkling_snakes.db.pgsql_db.sessionmaker')
    def test__get_session_proper_route(self, sessionmaker_mock: mock.MagicMock):
        self.db_client._engine = mock.Mock()
        session_mock = mock.Mock()
        sessionmaker_return_value_mock = mock.Mock(return_value=session_mock)
        sessionmaker_mock.return_value = sessionmaker_return_value_mock

        session = self.db_client._get_session()

        self.assertIs(session, session_mock)
        sessionmaker_mock.assert_called_once_with(bind=self.db_client._engine)
        sessionmaker_return_value_mock.called_once()

    @mock.patch('sparkling_snakes.db.pgsql_db.Metadata', mock.Mock(id='some_id'))
    @mock.patch('sparkling_snakes.db.pgsql_db.log')
    def test_metadata_exists_by_id_exceptions(self, log_mock: mock.MagicMock):
        log_mock.exception = mock.Mock()
        self.db_client._get_session = mock.Mock(side_effect=[NoResultFound, SQLAlchemyError])

        self.assertFalse(self.db_client.metadata_exists_by_id('object_id_1'))
        with self.assertRaises(SQLAlchemyError):
            self.db_client.metadata_exists_by_id('object_id_2')
        log_mock.exception.assert_called_once()
