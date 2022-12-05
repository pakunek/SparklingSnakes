import math

import botocore.exceptions
from fastapi import HTTPException

from sparkling_snakes import consts
from sparkling_snakes.api.models.schemas.tasks import TaskInResponse, TaskInCreate
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper
from sparkling_snakes.helpers.s3_helper import S3Helper
from sparkling_snakes.processor.pyspark_functions import pyspark_file_flow
from sparkling_snakes.utils import map_and_filter_s3_objects


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
        pyspark_session = pyspark_helper.get_session()

        files_per_prefix = math.floor(task.files_total / len(consts.EXPECTED_S3_PREFIXES))

        for prefix in consts.EXPECTED_S3_PREFIXES:
            try:
                for page in S3Helper.get_page_iterator(task.region_name,
                                                       task.bucket_name,
                                                       f'{prefix}/',
                                                       files_per_prefix):
                    prepared_s3_items = map_and_filter_s3_objects(page['Contents'])
                    task_data = pyspark_session.sparkContext.parallelize(prepared_s3_items)
                    task_data.foreach(lambda x: pyspark_file_flow(x, task, config))
            except botocore.exceptions.ClientError:
                raise HTTPException(status_code=503, detail="AWS/S3 does not work properly, cannot continue")
            except botocore.exceptions.ParamValidationError:
                raise HTTPException(status_code=400, detail="Provided AWS/S3 parameters are invalid")
        return TaskInResponse(message="File(s) metadata stored properly")
