import math

import boto3
from botocore.handlers import disable_signing

from sparkling_snakes import consts
from sparkling_snakes.api.models.schemas.tasks import TaskInResponse, TaskInCreate
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper


# TODO: Cleanup, preferably inject/reuse helpers, split pyspark code from business logic,handle exceptions,
# TODO: extract boto3 code to helper
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


# TODO: Move, divide onto smaller parts, wrap with classes/objects, extract common logic, think about processing tools
# TODO: to use in all scenarios. Prepare directory for files, cleanup after processing. Finally store metadata in DB.
# TODO: Add dir checks (preferably pre app load), handle exceptions
def process_file(s3obj_key: str, task: TaskInCreate) -> None:
    s3_resource = boto3.resource(service_name='s3', region_name=task.region_name)
    s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

    file_path = f'{consts.FILE_STORAGE}/{s3obj_key.split("/")[-1]}'
    s3_resource.Bucket(task.bucket_name).download_file(s3obj_key, file_path)
