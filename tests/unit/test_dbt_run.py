from unittest.mock import patch

import pytest

from pre_commit_dbt.dbt_run import main
from pre_commit_dbt.dbt_run import prepare_cmd


def test_dbt_run():
    with patch("pre_commit_dbt.utils.subprocess.Popen") as mock_popen:
        mock_popen.return_value.communicate.return_value = (
            b"stdout",
            b"stderr",
        )
        mock_popen.return_value.returncode = 0
        result = main(("test",))
        assert result == 0


def test_dbt_run_error():
    with patch("pre_commit_dbt.utils.subprocess.Popen") as mock_popen:
        mock_popen.return_value.communicate.return_value = (
            b"stdout",
            b"stderr",
        )
        mock_popen.return_value.returncode = 1
        result = main(("test",))
        assert result == 1


@pytest.mark.parametrize(
    "files,global_flags,cmd_flags,expected",
    [
        (["/aa/bb/cc.txt"], None, None, ["dbt", "run", "-m", "cc"]),
        (
            ["/aa/bb/cc.txt"],
            ["++debug", "++no-write-json"],
            None,
            ["dbt", "--debug", "--no-write-json", "run", "-m", "cc"],
        ),
        (
            ["/aa/bb/cc.txt"],
            None,
            ["+t", "prod"],
            ["dbt", "run", "-m", "cc", "-t", "prod"],
        ),
        (
            ["/aa/bb/cc.txt"],
            "",
            ["+t", "prod"],
            ["dbt", "run", "-m", "cc", "-t", "prod"],
        ),
    ],
)
def test_dbt_run_cmd(files, global_flags, cmd_flags, expected):
    result = prepare_cmd(files, global_flags, cmd_flags)
    assert result == expected
