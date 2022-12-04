import math
from typing import Any

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes.api.models.schemas.tasks import TaskInResponse, TaskInCreate
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper
from sparkling_snakes.processor.file_processor import FileProcessor


# TODO: Cleanup, preferably inject/reuse helpers, handle exceptions
class TasksService:
    @staticmethod
    def run_task(task: TaskInCreate) -> TaskInResponse:
        config = AppConfigHelper().get_config()
        pyspark_helper = PySparkHelper(config)

        ss = pyspark_helper.get_session()
        sc = ss.sparkContext

        s3_resource = boto3.resource(service_name='s3', region_name=task.region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

        file_count = math.floor(task.n/2)

        # TODO: Handle higher n values either by builtin boto3 paging or own code
        # TODO: Handle second set of files
        healthy_object_summaries = [
            s3obj.key
            for s3obj
            in s3_resource.Bucket(task.bucket_name).objects.filter(Prefix='0/',
                                                                   Marker='0/00Tree.html').limit(file_count)
        ]
        task_data = sc.parallelize(healthy_object_summaries)

        # TODO: Cannot pickle SSLContext, hence the bucket connection needs to be re-established within task
        # TODO: Think about a better way to do it, it seems to be redundant
        task_data.foreach(lambda s3obj_key: process_file(s3obj_key, task, config))
        return TaskInResponse(message="File(s) downloaded properly")


# TODO: Store metadata in DB. Handle exceptions
def process_file(s3obj_key: str, task: TaskInCreate, config: dict[str, Any]) -> None:
    file_processor = FileProcessor(s3obj_key, task.region_name, task.bucket_name)
    file_processor.init_storage()
    file_processor.init_s3_connection()
    file_processor.init_db_connection(config)

    if file_processor.needs_to_be_processed():
        file_processor.download_file()
        _ = file_processor.process()
