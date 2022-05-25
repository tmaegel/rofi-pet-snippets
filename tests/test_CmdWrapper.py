# coding=utf-8
import pytest

from rofi_pet_snippets import check_dependency
from rofi_pet_snippets.cmd import CmdWrapper


def test_run_cmd__success():
    cmd = ["echo", "-n", "test"]
    out, err, ret = CmdWrapper.run_cmd(cmd)
    assert out == "test"
    assert err is None
    assert ret == 0


def test_run_cmd__error_cmd_not_found():
    cmd = ["echo1", "test"]
    with pytest.raises(RuntimeError):
        CmdWrapper.run_cmd(cmd)


def test_run_cmd__error_invalid_arg():
    cmd = ["pwd", "--invalid-arg"]
    with pytest.raises(RuntimeError):
        CmdWrapper.run_cmd(cmd)


def test_run_cmd__error_cmd_failed():
    cmd = ["ls", "abc"]
    with pytest.raises(RuntimeError):
        CmdWrapper.run_cmd(cmd)


def test_check_dependency__valid():
    assert check_dependency("pwd") is True


def test_check_dependency__invalid():
    with pytest.raises(SystemExit) as wrapped_exit:
        check_dependency("pwd1")
    assert wrapped_exit.type == SystemExit
    assert wrapped_exit.value.code == 1
