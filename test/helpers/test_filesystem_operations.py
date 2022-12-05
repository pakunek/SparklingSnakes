import unittest
from unittest import mock

from sparkling_snakes.exceptions import InvalidFile
from sparkling_snakes.helpers.filesystem_operations import FilesystemOperationsHelper


class TestFilesystemOperationsHelper(unittest.TestCase):
    @mock.patch('sparkling_snakes.helpers.filesystem_operations.FilesystemOperationsHelper.file_exists',
                mock.Mock(return_value=True))
    @mock.patch('sparkling_snakes.helpers.filesystem_operations.subprocess')
    def test__run_command_if_file_exists_proper_route(self, subprocess_mock):
        subprocess_mock.PIPE = 'expected_pipe_value'
        subprocess_mock.run = mock.Mock()

        FilesystemOperationsHelper._run_command_if_file_exists('some/very/existing/path', 'not rm -rf /')
        subprocess_mock.run.assert_has_calls(
            [mock.call('not rm -rf /', stdout='expected_pipe_value', stderr='expected_pipe_value',
                       universal_newlines=True, shell=True)]
        )

    @mock.patch('sparkling_snakes.helpers.filesystem_operations.FilesystemOperationsHelper.file_exists',
                mock.Mock(return_value=False))
    def test_invalid_file_exception(self):
        with self.assertRaises(InvalidFile):
            FilesystemOperationsHelper._run_command_if_file_exists('/', 'ls')
