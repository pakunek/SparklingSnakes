from sparkling_snakes import consts


def is_key_supported(s3_key: str) -> bool:
    return any(s3_key.endswith(key_extension) for key_extension in consts.SUPPORTED_S3_KEY_EXTENSIONS)
