from dataclasses import dataclass

from sparkling_snakes import consts


# TODO: To be revised, might be redundant since PySpark has own DataFrames
@dataclass
class FileMetadata:
    imports: int = consts.DEFAULT_DB_INT_VALUE
    exports: int = consts.DEFAULT_DB_INT_VALUE
    path: str = consts.DEFAULT_DB_STR_VALUE
    type: str = consts.DEFAULT_DB_STR_VALUE
    arch: str = consts.DEFAULT_DB_STR_VALUE
