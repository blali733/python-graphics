from unittest.mock import patch

import pytest

from src.osutils import pathtools


class TestPathtools:
    win_string = "d:\\python\\path\\test\\app"
    posix_string = "/python/path/test/app"

    @patch("src.osutils.pathtools.os_name", "posix")
    def test_get_folder_name_from_path_posix_reverse_addressing(self):
        assert "test" == pathtools.get_folder_name_from_path(self.posix_string, -2)

    @patch("src.osutils.pathtools.os_name", "posix")
    def test_get_folder_name_from_path_posix_normal_addressing(self):
        assert "test" == pathtools.get_folder_name_from_path(self.posix_string, 3)

    @patch("src.osutils.pathtools.os_name", "posix")
    def test_get_folder_name_from_path_posix_exception_range_violation(self):
        with pytest.raises(IndexError) as e_info:
            assert "test" == pathtools.get_folder_name_from_path(self.posix_string, 10)
        assert "Index not in range!" in str(e_info.value)

    @patch("src.osutils.pathtools.os_name", "nt")
    def test_get_folder_name_from_path_windows_reverse_addressing(self):
        assert "test" == pathtools.get_folder_name_from_path(self.win_string, -2)

    @patch("src.osutils.pathtools.os_name", "nt")
    def test_get_folder_name_from_path_windows_normal_addressing(self):
        assert "test" == pathtools.get_folder_name_from_path(self.win_string, 3)

    @patch("src.osutils.pathtools.os_name", "nt")
    def test_get_folder_name_from_path_windows_exception_range_violation(self):
        with pytest.raises(IndexError) as e_info:
            assert "test" == pathtools.get_folder_name_from_path(self.win_string, 10)
        assert "Index not in range!" in str(e_info.value)
