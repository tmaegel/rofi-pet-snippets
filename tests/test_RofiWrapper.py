#!/usr/bin/env python3
# coding=utf-8

import pytest
from conftest import mockenv, mockenvclear

from rofi_pet_snippets.rofi import RofiWrapper


def test_rofi_output__valid_1(capsys):
    RofiWrapper.output("hallo")
    captured = capsys.readouterr()
    assert captured.out == "hallo\0\n"


def test_rofi_output__valid_2(capsys):
    RofiWrapper.output("hallo", info="abc")
    captured = capsys.readouterr()
    assert captured.out == "hallo\0info\x1fabc\n"


def test_rofi_output__valid_3(capsys):
    RofiWrapper.output("hallo", meta="xyz")
    captured = capsys.readouterr()
    assert captured.out == "hallo\0meta\x1fxyz\n"


def test_rofi_output__valid_4(capsys):
    RofiWrapper.output("hallo", info="abc", meta="xyz")
    captured = capsys.readouterr()
    assert captured.out == "hallo\0info\x1fabc\x1fmeta\x1fxyz\n"


@mockenv(ROFI_RETV="0")
def test_rofi_first_call__valid_1():
    result = RofiWrapper.first_call()
    assert result is True


@mockenv(ROFI_RETV="1")
def test_rofi_first_call__valid_2():
    result = RofiWrapper.first_call()
    assert result is False


@mockenv(ROFI_INFO="info")
def test_rofi_get_info__valid():
    info = RofiWrapper.get_info()
    assert info == "info"


@mockenvclear()
def test_rofi_get_info__invalid():
    with pytest.raises(SystemExit) as wrapped_exit:
        _ = RofiWrapper.get_info()
    assert wrapped_exit.type == SystemExit
    assert wrapped_exit.value.code == 1
