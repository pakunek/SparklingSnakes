import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes import consts
from sparkling_snakes.db.generic_db import GenericDatabase
from sparkling_snakes.db.pgsql_db import PostgreSQLDatabase
from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper
from sparkling_snakes.processor.data_models import FileMetadata

log = logging.getLogger(__name__)


class FileProcessor:
    """Main file processing class."""

    def __init__(self, s3object_key: str, s3_region_name: str, s3_bucket_name: str):
        # Init parameters
        self._object_key = s3object_key
        self._region_name = s3_region_name
        self._bucket_name = s3_bucket_name
        self._local_file_path = f'{consts.FILE_STORAGE}/{s3object_key.split("/")[-1]}'

        # Future use variables
        self._s3_e_tag: Optional[str] = None
        self._bucket: Optional[Any] = None
        self._database: Optional[GenericDatabase] = None

        self._operations = {
            'exports': {
                'func': FilesystemOperationsHelper.get_function_exports_count,
                'args': self._local_file_path
            },
            'imports': {
                'func': FilesystemOperationsHelper.get_function_imports_count,
                'args': self._local_file_path
            },
            'size': {
                'func': FilesystemOperationsHelper.get_file_size,
                'args': self._local_file_path
            },
            'type': {
                'func': FilesystemOperationsHelper.get_file_type,
                'args': self._local_file_path
            },
            'arch': {
                'func': FilesystemOperationsHelper.get_architecture,
                'args': self._local_file_path
            }
        }

    def init_s3_connection(self) -> None:
        """Initialize s3 connection via boto3."""
        s3_resource = boto3.resource(service_name='s3', region_name=self._region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        self._bucket = s3_resource.Bucket(self._bucket_name)

    def init_db_connection(self, config: dict[str, Any]) -> None:
        """Initialize DB connection.

        :param config: app configuration dict
        """
        self._database = PostgreSQLDatabase()
        self._database.init_connection(config)

    def needs_to_be_processed(self) -> bool:
        """Indicate if file needs to be processed."

        :return: True if file needs processing. False otherwise.
        """
        return not self._database.metadata_exists_by_id(self._s3_e_tag)

    def store_s3_e_tag(self) -> None:
        """Prepare e_tag for processed key.

        S3 e_tag will be used for further processing as unique ID. This assumes that
        hash function generating e_tag is not a trivial one. Otherwise, some keys
        might not be processed due to falsy hash matches.
        """
        self._s3_e_tag = self._bucket.Object(self._object_key).e_tag

    def download_file(self) -> None:
        """Download file from pre-configured S3 bucket."""
        self._bucket.download_file(self._object_key, self._local_file_path)
        log.info("File for key %s downloaded properly", self._object_key)

    def store_in_db(self, file_metadata: FileMetadata) -> None:
        """Store file's metadata using pre-configured DB object.

        :param file_metadata: dataclass containing file's metadata
        """
        self._database.put_metadata(self._s3_e_tag, file_metadata)
        log.info("Stored DB entry for %s", self._object_key)

    def process(self) -> FileMetadata:
        """Run all required operations in parallel.

        Basing on pre-defined list of operations to be made, runs all of them in
        parallel (the majority of them is IO-based so performance gain is expected).

        :return: FileMetadata object with all values filled
        """
        with ThreadPoolExecutor(len(self._operations)) as pool_executor:
            operation_futures = [pool_executor.submit(self._operations[operation]['func'],
                                                      self._operations[operation]['args'])
                                 for operation in self._operations]
            final_results = dict(zip(self._operations.keys(),
                                     [operation_future.result() for operation_future in operation_futures]))
            log.info("File for key %s processed properly", self._object_key)

            file_metadata = FileMetadata(**final_results)
            file_metadata.path = self._local_file_path
            return file_metadata
