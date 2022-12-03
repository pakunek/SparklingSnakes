import os
import subprocess

from sparkling_snakes.processor.exceptions import InvalidFile


class FilesystemOperationsHelper:
    readpe_get_imports_command_template: str = 'readpe -i -f xml {} | grep -e "<object name=\\"Function\\">" | wc -l'
    readpe_get_exports_command_template: str = 'readpe -e -f xml {} | grep -e "<object name=\\"Function\\">" | wc -l'

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """Recursively create given directory path.

        Does nothing if directory already exists.

        :param directory_path: path of a directory to create given in string
        :return: None
        """
        os.makedirs(directory_path, exist_ok=True)

    @staticmethod
    def count_function_imports(file_path: str) -> int:
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
        read_imports_command: str = FilesystemOperationsHelper.readpe_get_imports_command_template.format(file_path)
        result = FilesystemOperationsHelper._run_command_if_file_exists(file_path, read_imports_command)

        return int(stdout) if (stdout := result.stdout) and not result.stderr else -1

    @staticmethod
    def count_function_exports(file_path: str) -> int:
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
        read_exports_command: str = FilesystemOperationsHelper.readpe_get_exports_command_template.format(file_path)
        result = FilesystemOperationsHelper._run_command_if_file_exists(file_path, read_exports_command)

        return int(stdout) if (stdout := result.stdout) and not result.stderr else -1

    @staticmethod
    def _run_command_if_file_exists(file_path: str,
                                    cmd: str) -> subprocess.CompletedProcess | subprocess.CompletedProcess[str]:
        """Run given command if provided file exists.

        :param file_path: file path to be checked
        :param cmd: cmd to be executed if file exists
        :return: raw subprocess.run output
        """
        if not os.path.isfile(file_path):
            raise InvalidFile(file_path=file_path)

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True, shell=True)
        return result
