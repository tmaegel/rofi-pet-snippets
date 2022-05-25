# coding=utf-8
from unittest.mock import patch

import pytest
from conftest import mockenv, mockenvclear

from rofi_pet_snippets import main


@mockenvclear()
def test_main__invalid():
    with patch(
        "rofi_pet_snippets.parse_args",
        return_value={
            "debug": False,
            "notify": False,
            "terminal": False,
        },
    ) as mocked_1:
        with patch(
            "rofi_pet_snippets.check_dependency",
            return_value=True,
        ) as mocked_2:
            with pytest.raises(SystemExit) as wrapped_exit:
                main()
            assert wrapped_exit.type == SystemExit
            assert wrapped_exit.value.code == 1
            mocked_1.assert_called_once()
            assert mocked_2.call_count > 0


@mockenv(ROFI_RETV="0")
def test_main__first_call__valid(capsys):
    with patch(
        "rofi_pet_snippets.parse_args",
        return_value={
            "debug": False,
            "notify": False,
            "terminal": False,
        },
    ) as mocked_1:
        with patch(
            "rofi_pet_snippets.check_dependency",
            return_value=True,
        ) as mocked_2:
            with patch(
                "rofi_pet_snippets.PetWrapper.list_snippets",
                return_value=[
                    {
                        "description": "description1",
                        "command": "command1",
                        "tags": ["a1", "b1", "c1"],
                    }
                ],
            ) as mocked_3:
                main()
                captured = capsys.readouterr()
                assert "description1" in captured.out
                assert "command1" in captured.out
                assert "a1, b1, c1" in captured.out
                mocked_1.assert_called_once()
                assert mocked_2.call_count > 0
                mocked_3.assert_called_once()


@mockenv(ROFI_RETV="0")
def test_main__first_call__empty():
    with patch(
        "rofi_pet_snippets.parse_args",
        return_value={
            "debug": False,
            "notify": False,
            "terminal": False,
        },
    ) as mocked_1:
        with patch(
            "rofi_pet_snippets.check_dependency",
            return_value=True,
        ) as mocked_2:
            with patch(
                "rofi_pet_snippets.PetWrapper.list_snippets",
                return_value=[],
            ) as mocked_3:
                with pytest.raises(SystemExit) as wrapped_exit:
                    main()
                assert wrapped_exit.type == SystemExit
                assert wrapped_exit.value.code == 0
                mocked_1.assert_called_once()
                assert mocked_2.call_count > 0
                mocked_3.assert_called_once()


@mockenv(ROFI_RETV="1")
def test_main__second_call__valid():
    with patch(
        "rofi_pet_snippets.parse_args",
        return_value={
            "debug": False,
            "notify": False,
            "terminal": False,
        },
    ) as mocked_1:
        with patch(
            "rofi_pet_snippets.check_dependency",
            return_value=True,
        ) as mocked_2:
            with patch(
                "rofi_pet_snippets.RofiWrapper.get_info",
                return_value="info",
            ) as mocked_3:
                with patch(
                    "rofi_pet_snippets.CmdWrapper.run_detached_cmd",
                    return_value=True,
                ) as mocked_4:
                    main()
                    mocked_1.assert_called_once()
                    assert mocked_2.call_count > 0
                    mocked_3.assert_called_once()
                    assert mocked_4.call_count > 0
