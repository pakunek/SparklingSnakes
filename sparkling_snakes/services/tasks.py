import math
from typing import Any

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes import consts
from sparkling_snakes.api.models.schemas.tasks import TaskInResponse, TaskInCreate
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper
from sparkling_snakes.processor.file_processor import FileProcessor


# TODO: Cleanup, preferably inject/reuse helpers, handle exceptions
class TasksService:
    """Service for task execution."""
    @staticmethod
    def run_task(task: TaskInCreate) -> TaskInResponse:
        """Run 'Task'.

        Method initializes all connections (unless initialized previously) to services required to:
         * Get list of bucket keys
         * Check if objects under keys are already processed
         * Process unprocessed files using PySpark
         * Store the result of processing in DB of choice

        :param task: TaskInCreate model containing data vital for Task execution
        :return: TaskInResponse object (if HTTP timeout was not hit which is likely to happen with bigger Tasks)
        """
        config = AppConfigHelper().get_config()
        pyspark_helper = PySparkHelper(config)

        ss = pyspark_helper.get_session()

        s3_resource = boto3.resource(service_name='s3', region_name=task.region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        s3_bucket = s3_resource.Bucket(task.bucket_name)

        files_per_prefix = math.floor(task.n/2)

        # TODO: Handle higher n values either by builtin boto3 paging or own code
        # TODO: Handle second set of files
        prefix_summaries = [
            s3obj.key for s3obj in s3_bucket.objects.filter(Prefix='0/', Marker='0/00Tree.html').limit(files_per_prefix)
        ]
        task_data = ss.sparkContext.parallelize(prefix_summaries)

        # TODO: Cannot pickle SSLContext, hence the bucket connection needs to be re-established within task
        # TODO: Think about a better way to do it, it seems to be redundant
        task_data.foreach(lambda s3obj_key: pyspark_file_flow(s3obj_key, task, config))
        return TaskInResponse(message="File(s) downloaded properly")


# TODO: Handle exceptions
def pyspark_file_flow(s3obj_key: str, task: TaskInCreate, config: dict[str, Any]) -> None:
    """Run whole flow for given file.

    Due to issues with pickling of i.e. SSLContext, some connections and objects
    need to be (re)created within this function since it is destined to run under
    PySpark environment.

    :param s3obj_key: S3 Bucket key pointing to one specific PE file
    :param task: user-given data required for connection
    :param config: app configuration dict
    """
    FilesystemOperationsHelper.create_directory(consts.FILE_STORAGE)
    file_processor = FileProcessor(s3obj_key, task.region_name, task.bucket_name)
    file_processor.init_s3_connection()
    file_processor.init_db_connection(config)
    file_processor.store_s3_e_tag()

    if file_processor.needs_to_be_processed():
        file_processor.download_file()
        file_metadata = file_processor.process()
        file_processor.store_in_db(file_metadata)
