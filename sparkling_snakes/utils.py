from sparkling_snakes import consts
from sparkling_snakes.processor.data_models import S3Item


def is_key_supported(s3_key: str) -> bool:
    """Verify if given s3 key is supported.

    Using generator instead of list should increase the performance *a bit*, especially
    if the list grows.

    :param s3_key: s3_key as string
    :return: True or False depending on existence in consts.UNSUPPORTED_S3_KEY_EXTENSIONS list
    """
    return not any(s3_key.lower().endswith(key_extension) for key_extension in consts.UNSUPPORTED_S3_KEY_EXTENSIONS)


def map_and_filter_s3_objects(page_contents: list[dict[str, str | int]]) -> list[S3Item]:
    """Map and filter s3 objects to S3Items.

    Checks if objects provided are supported by the processor and maps them
    to values vital for further processing which are Key and ETag enclosed
    in prepared S3Item dataclass.

    :param page_contents: page['Contents'] object - a product of boto3/s3 pagination usage
    :return: list of S3Item dataclass(es)
    """
    return filter(lambda x: is_key_supported(x.s3_key), map(lambda y: S3Item(y['Key'], y['ETag']), page_contents))
