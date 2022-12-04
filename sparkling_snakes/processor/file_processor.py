import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes import consts
from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper
from sparkling_snakes.processor.data_models import FileMetadata


class FileProcessor:

    def __init__(self, s3object_key: str, s3_region_name: str, s3_bucket_name: str):
        self._object_key = s3object_key
        self._region_name = s3_region_name
        self._bucket_name = s3_bucket_name

        self._local_file_path = f'{consts.FILE_STORAGE}/{s3object_key.split("/")[-1]}'

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

    def init_s3_connection(self):
        s3_resource = boto3.resource(service_name='s3', region_name=self._region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        s3_resource.Bucket(self._bucket_name).download_file(self._object_key, self._local_file_path)

    # TODO: Actually do the check (s3 hash? s3 bucket+region+name? to be determined) processing
    def needs_processing(self) -> bool:
        return True

    def process(self) -> FileMetadata:
        """Run all required operations in parallel.

        Basing on pre-defined list of operations to be made, runs all of them in
        parallel (the majority of them is IO-based so performance gain is expected).

        :return: FileMetadata object with filled values
        """
        with ThreadPoolExecutor(min(len(self._operations), multiprocessing.cpu_count() - 1)) as pool_executor:
            operation_futures = [pool_executor.submit(self._operations[operation]['func'],
                                                      self._operations[operation]['args'])
                                 for operation in self._operations]
            final_results = dict(zip(self._operations.keys(),
                                     [operation_future.result() for operation_future in operation_futures]))
            return FileMetadata(**final_results)
