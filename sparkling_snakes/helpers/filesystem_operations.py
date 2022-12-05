import os
import subprocess
from functools import lru_cache
from typing import Callable, Any

from sparkling_snakes import consts
from sparkling_snakes.exceptions import InvalidFile
from sparkling_snakes.processor.data_models import ExiftoolOutput


class FilesystemOperationsHelper:
    """File/Directory management class."""

    imports_command_template: str = 'readpe -i -f xml {} | grep -e "<object name=\\"Function\\">" | wc -l'
    exports_command_template: str = 'readpe -e -f xml {} | grep -e "<object name=\\"Function\\">" | wc -l'
    exiftool_command_template: str = 'exiftool -filesize# -filetypeextension -machinetype -s -s {}'

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """Recursively create given directory path.

        Does nothing if directory already exists.

        :param directory_path: path of a directory to create given in string
        :return: None
        """
        os.makedirs(directory_path, exist_ok=True)

    @staticmethod
    @lru_cache(maxsize=consts.EXPECTED_OPERATIONS_PER_FILE)
    def file_exists(file_path: str) -> bool:
        """Check if file exists.

        Method created for sake of performance. Since multiple methods require the file to exist,
        it is worth to wrap it with cache and trust that the file did not disappear in dockerized environment.

        :param file_path: path of file to be checked for existence
        :return: bool
        """
        return os.path.isfile(file_path)

    @staticmethod
    def get_function_imports_count(file_path: str) -> int:
        """Count file's function imports.

        Calls subprocess shell command to read the number of PE File's imported functions. Bases on:
         * readpe   (output intentionally set to *.xml for easier parsing purpose, skipping *.xml unmarshalling for
                    performance reasons - thus trading quality of solution for better performance which is expected)
         * grep     searches for <object name="Function"> pattern indicating new nodes in *.xml file structure
         * wc       counting the lines and printing the final product which is a number of imported functions

        :param file_path: path of PE File to be processed
        :raises InvalidFile: raised if provided file_path does not map to any file
        :return: number of function imports which given file consists of
        """
        read_imports_command: str = FilesystemOperationsHelper.imports_command_template.format(file_path)
        result = FilesystemOperationsHelper._run_command_if_file_exists(file_path, read_imports_command)
        return FilesystemOperationsHelper._sanitize_stdout(result, int, consts.DEFAULT_DB_INT_VALUE)

    @staticmethod
    def get_function_exports_count(file_path: str) -> int:
        """Count file's function exports.

        Calls subprocess shell command to read the number of PE File's exported functions. Bases on:
         * readpe   (output intentionally set to *.xml for easier parsing purpose, skipping *.xml unmarshalling for
                    performance reasons - thus trading quality of solution for better performance which is expected)
         * grep     searches for <object name="Function"> pattern indicating new nodes in *.xml file structure
         * wc       counting the lines and printing the final product which is a number of exported functions

        :param file_path: path of PE File to be processed
        :raises InvalidFile: raised if provided file_path does not map to any file
        :return: number of function exports which given file consists of
        """
        read_exports_command: str = FilesystemOperationsHelper.exports_command_template.format(file_path)
        result = FilesystemOperationsHelper._run_command_if_file_exists(file_path, read_exports_command)
        return FilesystemOperationsHelper._sanitize_stdout(result, int, consts.DEFAULT_DB_INT_VALUE)

    @staticmethod
    def get_file_size(file_path: str) -> str:
        """Get file size.

        Intentionally using string format in order to prevent potential int overflow issues in DB.

        :param file_path: path of file to be checked against size
        :return: file size in bytes as string
        """
        return FilesystemOperationsHelper._get_exiftool_data(file_path).file_size

    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Get file type.

        :param file_path: path of file to be checked against its extension type
        :return: file type without delimiters and whitespace as string
        """
        return FilesystemOperationsHelper._get_exiftool_data(file_path).file_type

    @staticmethod
    def get_architecture(file_path: str) -> str:
        """Get file architecture.

        :param file_path: path of file to be checked against its architecture
        :return: file architecture reduced to 'x64' and 'x86' values as string
        """
        return FilesystemOperationsHelper._get_exiftool_data(file_path).architecture

    # TODO: Verify if caching works properly within ThreadPoolExecutioner context
    @staticmethod
    @lru_cache(maxsize=len(consts.ExiftoolSupportedFields))
    def _get_exiftool_data(file_path: str) -> ExiftoolOutput:
        """Get data available through exiftool.

        Calls subprocess shell command to read:
         * FileSize                     -   in bytes
         * FileTypeExtension            -   simple extension without delimiters
         * MachineType (Architecture)   -   full unmapped MachineType
        Bases on:
         * exiftool Provides all data mentioned above (exclusively). The output format is
                    shortened with double -s for further parsing purposes.

        Since this method is responsible for multiple values, it has been cached in order
        to reuse the first call.

        :param file_path: path of PE File to be processed
        :raises InvalidFile: raised if provided file_path does not map to any file
        :return: number of function exports which given file consists of
        """
        read_exports_command: str = FilesystemOperationsHelper.exiftool_command_template.format(file_path)
        result = FilesystemOperationsHelper._run_command_if_file_exists(file_path, read_exports_command)
        if (stdout := result.stdout) and not stdout.isspace() and not result.stderr:
            return FilesystemOperationsHelper._map_exiftool_output(stdout)
        return ExiftoolOutput()

    @staticmethod
    def _map_exiftool_output(stdout: str) -> ExiftoolOutput:
        """Map exiftool output to ExiftoolOutput instance.

        :param stdout: clean exiftool output shortened by double '-s' parameter
        :return: instance of ExiftoolOutput with non-existing values filled by defaults
        """
        exiftool_output = ExiftoolOutput()

        for line in stdout.splitlines():
            match (split_line := line.strip().split(' ', maxsplit=1))[0].rstrip(':'):
                case consts.ExiftoolSupportedFields.file_size.value:
                    exiftool_output.file_size = split_line[-1]
                case consts.ExiftoolSupportedFields.file_type.value:
                    exiftool_output.file_type = split_line[-1]
                case consts.ExiftoolSupportedFields.architecture.value:
                    exiftool_output.architecture = consts.EXIFTOOL_ARCHITECTURE_MAPPING.get(split_line[-1],
                                                                                            consts.DEFAULT_DB_STR_VALUE)
        return exiftool_output

    @staticmethod
    def _run_command_if_file_exists(file_path: str,
                                    cmd: str) -> subprocess.CompletedProcess | subprocess.CompletedProcess[str]:
        """Run given command if provided file exists.

        :param file_path: file path to be checked
        :param cmd: cmd to be executed if file exists
        :raises InvalidFile: raised if provided file_path does not map to any file
        :return: raw subprocess.run output
        """
        if not FilesystemOperationsHelper.file_exists(file_path):
            raise InvalidFile(file_path=file_path)
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)

    @staticmethod
    def _sanitize_stdout(result: subprocess.CompletedProcess | subprocess.CompletedProcess[str],
                         return_type: Callable,
                         default: str | int) -> Any:
        """Verify & cast output if valid.

        Simple method for code deduplication purposes.

        :param result: subprocess.run output
        :param return_type: function indicating the type to which stdout should be cast
        :param default: default value to return if stdout is invalid for whatever reason
        :return: default or stdout cast onto given type
        """
        if (stdout := result.stdout) and not stdout.isspace() and not result.stderr:
            return return_type(stdout)
        return default
