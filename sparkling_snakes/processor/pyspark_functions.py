"""Functions ready to be used as PySpark actions."""

from sparkling_snakes.api.models.schemas.tasks import TaskInCreate
from sparkling_snakes.processor.data_models import S3Item
from sparkling_snakes.processor.file_processor import FileProcessor
from sparkling_snakes.processor.types import Config


def pyspark_file_flow(s3_item: S3Item, task: TaskInCreate, config: Config) -> None:
    """Run whole flow for given file.

    Due to issues with pickling of i.e. SSLContext, some connections and objects
    need to be (re)created within this function since it is destined to run under
    PySpark environment.

    :param s3_item: S3Item object with Key and ETag
    :param task: user-given data required for connection
    :param config: app configuration dict
    """
    file_processor = FileProcessor(s3_item, task.region_name, task.bucket_name)
    file_processor.init_db_connection(config)

    if file_processor.needs_to_be_processed():
        file_processor.init_s3_connection()
        file_processor.download_file()
        file_metadata = file_processor.process()
        file_processor.store_in_db(file_metadata)
