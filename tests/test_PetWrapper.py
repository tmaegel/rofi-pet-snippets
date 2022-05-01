#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import patch

from rofi_pet_snippets import PetWrapper


@patch(
    "rofi_pet_snippets.PetWrapper.run_cmd",
    return_value=(
        """
        Description: description
        Command: command
        Tag: c b a
        """,
        "",
        0,
    ),
)
def test_list_cards__valid(mock):
    snippets = PetWrapper.list_snippets()
    for snippet in snippets:
        assert snippet["description"] == "description"
        assert snippet["command"] == "command"
        assert snippet["tags"] == ["a", "b", "c"]
    mock.assert_called_once()


@patch(
    "rofi_pet_snippets.PetWrapper.run_cmd",
    return_value=(
        """
        Description: description
        Command: command
        """,
        "",
        0,
    ),
)
def test_list_cards__valid_no_tags(mock):
    snippets = PetWrapper.list_snippets()
    for snippet in snippets:
        assert snippet["description"] == "description"
        assert snippet["command"] == "command"
        assert snippet["tags"] == []
    mock.assert_called_once()


@patch(
    "rofi_pet_snippets.PetWrapper.run_cmd",
    return_value=(
        """
        Description: description0
        Command: command0
        Tag: c0 b0 a0
        -----
        Description: description1
        Command: command1
        Tag: c1 b1 a1
        """,
        "",
        0,
    ),
)
def test_list_cards__valid_multiple(mock):
    snippets = PetWrapper.list_snippets()
    for i, snippet in enumerate(snippets):
        assert snippet["description"] == f"description{i}"
        assert snippet["command"] == f"command{i}"
        assert snippet["tags"] == [f"a{i}", f"b{i}", f"c{i}"]
    mock.assert_called_once()


@patch(
    "rofi_pet_snippets.PetWrapper.run_cmd",
    return_value=("", "", 0),
)
def test_list_cards__valid_empty(mock):
    snippets = PetWrapper.list_snippets()
    assert not snippets
    mock.assert_called_once()
