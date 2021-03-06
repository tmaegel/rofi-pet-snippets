# coding=utf-8
import os
import sys
from typing import Optional

from .log import logger


class RofiWrapper:
    def __init__(self, prompt: str, no_custom: bool = True):
        self.configure("prompt", prompt)
        self.configure("no-custom", str(no_custom).lower())
        self.configure("markup-rows", "true")

    @staticmethod
    def configure(key: str, value: str) -> None:
        print(f"\0{key}\x1f{value}")

    @staticmethod
    def output(
        entry: str, info: Optional[str] = None, meta: Optional[str] = None
    ) -> None:
        entry = entry + "\0"
        if info:
            entry = entry + "info\x1f" + info
        if meta:
            if "info\x1f" in entry:
                entry = entry + "\x1fmeta\x1f" + meta
            else:
                entry = entry + "meta\x1f" + meta
        print(entry)

    @staticmethod
    def first_call() -> bool:
        rofi_retv = os.getenv("ROFI_RETV", None)
        if not rofi_retv:
            logger.error("ROFI_RETV is not set.")
            sys.exit(1)
        if int(rofi_retv) == 0:
            return True

        return False

    @staticmethod
    def get_info() -> str:
        info = os.getenv("ROFI_INFO", None)
        if not info:
            logger.error("ROFI_INFO is not set.")
            sys.exit(1)

        return info
