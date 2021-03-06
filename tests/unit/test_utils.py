from pathlib import Path

import pytest

from pre_commit_dbt.utils import CalledProcessError
from pre_commit_dbt.utils import cmd_output
from pre_commit_dbt.utils import get_filenames
from pre_commit_dbt.utils import Model
from pre_commit_dbt.utils import ModelSchema
from pre_commit_dbt.utils import obj_in_child
from pre_commit_dbt.utils import paths_to_dbt_models
from pre_commit_dbt.utils import SourceSchema


def test_cmd_output_error():
    with pytest.raises(CalledProcessError):
        cmd_output("sh", "-c", "exit 1")


def test_cmd_output_output():
    ret = cmd_output("echo", "hi")
    assert ret == "hi\n"


@pytest.mark.parametrize(
    "test_input,pre,post,expected",
    [
        (["/aa/bb/cc.txt", "ee"], "", "", ["cc", "ee"]),
        (["/aa/bb/cc.txt"], "+", "", ["+cc"]),
        (["/aa/bb/cc.txt"], "", "+", ["cc+"]),
        (["/aa/bb/cc.txt"], "+", "+", ["+cc+"]),
    ],
)
def test_paths_to_dbt_models(test_input, pre, post, expected):
    result = paths_to_dbt_models(test_input, pre, post)
    assert result == expected


def test_paths_to_dbt_models_default():
    result = paths_to_dbt_models(["/aa/bb/cc.txt", "ee"])
    assert result == ["cc", "ee"]


@pytest.mark.parametrize(
    "obj,child_name,result",
    [
        (Model("aa", "bb", "cc", {}), "aa", True),
        (SourceSchema("aa", "bb", "cc", {}, {}), "source.aa.bb", True),
        (ModelSchema("aa", "model.aa", {}, Path("model.aa")), "model.aa", True),
        (object, "model.aa", False),
    ],
)
def test_obj_in_child(obj, child_name, result):
    assert obj_in_child(obj, child_name) == result


def test_get_filenames():
    result = get_filenames(["aa/bb/cc.sql", "bb/ee.sql"])
    assert result == {"cc": Path("aa/bb/cc.sql"), "ee": Path("bb/ee.sql")}
