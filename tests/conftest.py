#!/usr/bin/env python
# coding=utf-8

import os
from unittest import mock

import pytest


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)


def mockenvclear():
    return mock.patch.dict(os.environ, {}, clear=True)


@pytest.fixture
def get_value():
    value = 39
    return value
