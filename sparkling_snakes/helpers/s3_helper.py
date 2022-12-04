import boto3
from boto3_type_annotations.s3 import Bucket, Client, paginator
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing

from sparkling_snakes import consts


class S3Helper:
    """S3 connection helper class."""

    @staticmethod
    def get_bucket(region_name: str, bucket_name: str) -> Bucket:
        s3_resource = boto3.resource(service_name='s3', region_name=region_name)
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        return s3_resource.Bucket(bucket_name)

    @staticmethod
    def get_client(region_name: str) -> Client:
        return boto3.client('s3', region_name=region_name, config=Config(signature_version=UNSIGNED))

    @staticmethod
    def get_page_iterator(region_name: str, bucket_name: str, prefix: str, max_items: int) -> paginator:
        s3_paginator = S3Helper.get_client(region_name=region_name).get_paginator('list_objects')
        return s3_paginator.paginate(Bucket=bucket_name, Prefix=prefix, PaginationConfig={
            'MaxItems': max_items,
            'PageSize': consts.S3_PAGE_SIZE
        })
