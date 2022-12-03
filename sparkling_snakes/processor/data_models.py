from dataclasses import dataclass

# TODO: To be revised, might be redundant since PySpark has own DataFrames
@dataclass
class FileMetadata:
    path: str
    type: str
    arch: int
    imports: int
    exports: int
