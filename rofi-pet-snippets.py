#!/usr/bin/env python
# coding=utf-8

import logging
import logging.handlers
import os
import re
import subprocess
import sys
from typing import Tuple, Union

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address="/dev/log")
logger.addHandler(handler)
handler.setFormatter(logging.Formatter("%(name)10s - %(levelname)8s - %(message)s"))


class CmdWrapper:
    @staticmethod
    def run_cmd(
        cmd: list[str], pipe: bool = True
    ) -> Tuple[Union[str, None], Union[str, None], int]:
        out = None
        err = None
        proc = None
        try:
            with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE if pipe else subprocess.DEVNULL,
                stderr=subprocess.PIPE if pipe else subprocess.DEVNULL,
                # stdin=subprocess.PIPE if pipe else subprocess.DEVNULL,
            ) as proc:
                out, err = proc.communicate()
        except subprocess.CalledProcessError as exc:
            logger.critical("Error while running command '%s': %s", cmd, exc)
            raise RuntimeError(f"Error while running command '{cmd}': {exc}") from exc
        except FileNotFoundError as exc:
            logger.critical("Error while running command '%s': %s", cmd, exc)
            raise RuntimeError(f"Error while running command '{cmd}': {exc}") from exc
        finally:
            if proc and proc.returncode > 0:
                logger.critical(
                    "Error while running command '%s' [%s]: %s",
                    cmd,
                    proc.returncode,
                    err,
                )
                raise RuntimeError(
                    f"Error while running command '{cmd}' [{proc.returncode}]: {err}"
                )

        return (
            out.decode("utf-8") if out else None,
            err.decode("utf-8") if err else None,
            proc.returncode if proc else -1,
        )


class PetWrapper(CmdWrapper):
    @staticmethod
    def list_snippets():
        def reset_snippet():
            return {
                "description": "",
                "command": "",
                "tags": [],
            }

        snippet = reset_snippet()
        snippets = []
        out, _, _ = PetWrapper.run_cmd(["pet", "list"])
        if not out:
            return snippets
        command_regex = re.compile("^Command: (?P<command>.*)$")
        description_regex = re.compile("^Description: (?P<description>.*)$")
        tags_regex = re.compile("^Tag: (?P<tags>.*)$")
        for line in out.split("\n"):
            line = line.strip()
            if target := re.search(command_regex, line):
                snippet["command"] = target.groupdict()["command"]
            elif target := re.search(description_regex, line):
                snippet["description"] = target.groupdict()["description"]
            elif target := re.search(tags_regex, line):
                snippet["tags"] = target.groupdict()["tags"].split(" ")
                snippet["tags"].sort()
            else:
                if snippet["description"] and snippet["command"]:
                    snippets.append(snippet)
                    snippet = reset_snippet()

        return snippets


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
        entry: str, info: Union[str, None] = None, meta: Union[str, None] = None
    ) -> None:
        entry = f"{entry}"
        if info:
            entry = entry + f"\0info\x1f{info}"
        if meta:
            entry = entry + f"\0meta\x1f{meta}"
        print(entry)

    @staticmethod
    def get_value() -> Union[str, None]:
        try:
            return sys.argv[1]
        except KeyError:
            logger.error("No argument detected.")

        return None

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


def main() -> None:
    try:
        CmdWrapper.run_cmd(["which", "pet"])
    except RuntimeError:
        logger.error("pet is not installed on your system.")
        sys.exit(1)

    rofi = RofiWrapper(prompt="snippets >")
    if rofi.first_call():
        logger.info("rofi was called for the first time.")
        snippets = PetWrapper.list_snippets()
        if not snippets:
            logger.warning("No snippets were found.")
            sys.exit(0)
        for snippet in snippets:
            tags = ", ".join(snippet["tags"])
            entry = (
                f'<span font_size="medium">{snippet["description"]}</span>'
                + f' <span color="white" font_size="small">[ {tags} ]</span>'
            )
            rofi.output(entry, info=snippet["command"], meta=tags)
    else:
        info = rofi.get_info()
        logger.debug("Selected snippet %r", info)
        CmdWrapper.run_cmd(["wl-copy", info], pipe=False)
        CmdWrapper.run_cmd(["notify-send", "Snippet copied"])


if __name__ == "__main__":
    main()
