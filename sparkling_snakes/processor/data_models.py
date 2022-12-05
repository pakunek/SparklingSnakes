from dataclasses import dataclass

from sparkling_snakes import consts


@dataclass
class FileMetadata:
    imports: int = consts.DEFAULT_DB_INT_VALUE
    exports: int = consts.DEFAULT_DB_INT_VALUE
    path: str = consts.DEFAULT_DB_STR_VALUE
    size: str = consts.DEFAULT_DB_STR_VALUE
    type: str = consts.DEFAULT_DB_STR_VALUE
    arch: str = consts.DEFAULT_DB_STR_VALUE


class ExiftoolOutput:
    file_size: str = consts.DEFAULT_DB_STR_VALUE
    file_type: str = consts.DEFAULT_DB_STR_VALUE
    architecture: str = consts.DEFAULT_DB_STR_VALUE


@dataclass(frozen=True)
class S3Item:
    s3_key: str
    s3_e_tag: str
