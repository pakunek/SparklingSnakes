import math

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes.api.models.schemas.tasks import TaskInResponse, TaskInCreate
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper
from sparkling_snakes.processor.file_processor import FileProcessor


# TODO: Cleanup, preferably inject/reuse helpers, split pyspark code from business logic, handle exceptions
class TasksService:
    @staticmethod
    def run_task(task: TaskInCreate) -> TaskInResponse:
        config_helper = AppConfigHelper()
        pyspark_helper = PySparkHelper(config_helper.get_config())

        ss = pyspark_helper.get_session()
        sc = ss.sparkContext

        s3_resource = boto3.resource(service_name='s3', region_name=task.region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

        file_count = math.floor(task.n/2)

        # TODO: Handle higher n values either by builtin boto3 paging or own code
        # TODO: Think bucket creation is required here since it is re-created within the parallelized tasks anyway
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
        task_data.foreach(lambda s3obj_key: process_file(s3obj_key, task))
        return TaskInResponse(message=f"File(s) downloaded properly")


# TODO: Store metadata in DB. Prepare Technology-free DB Abstract class. Handle exceptions
def process_file(s3obj_key: str, task: TaskInCreate) -> None:
    file_processor = FileProcessor(s3obj_key, task.region_name, task.bucket_name)
    file_processor.init_s3_connection()

    if file_processor.needs_processing():
        _ = file_processor.process()
