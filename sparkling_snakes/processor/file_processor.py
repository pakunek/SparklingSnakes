import boto3
from botocore.handlers import disable_signing

from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper


# TODO: wip - should wrap all operations to be done for a single file
class FileProcessor:
    def __init__(self, s3object_key: str, s3_region_name: str, s3_bucket_name: str):
        self.object_key = s3object_key
        self.region_name = s3_region_name
        self.bucket_name = s3_bucket_name

    def init_s3_connection(self):
        file_storage = "/tmp/s3-files"
        FilesystemOperationsHelper.create_directory(file_storage)

        s3_resource = boto3.resource(service_name='s3', region_name=self.region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

        # TODO: Actual name of a file can be read using i.e. exiftool (already added to Dockerfile for later)
        s3_resource.Bucket(self.bucket_name).download_file(self.object_key,
                                                           f'{file_storage}/{self.object_key.split("/")[-1]}')

    # TODO: Actually do the check (s3 hash? s3 bucket+region+name? to be determined) processing
    def needs_processing(self) -> bool:
        return True

    def process(self):
        # TODO: start downloading
        # TODO: do other stuff (if any)
        # TODO: finish downloading
        # TODO: store in DB
        pass
