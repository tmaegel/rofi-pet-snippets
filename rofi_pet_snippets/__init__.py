#!/usr/bin/env python
# coding=utf-8

import sys

from .cmd import CmdWrapper
from .log import logger
from .pet import PetWrapper
from .rofi import RofiWrapper

VERSION = "0.0.1"


def check_dependency(cmd: str) -> bool:
    try:
        CmdWrapper.run_cmd(["which", cmd])
    except RuntimeError:
        logger.error("%s is not installed on your system.", cmd)
        sys.exit(1)

    return True


def main() -> None:
    check_dependency("pet")
    check_dependency("wl-copy")
    check_dependency("notify-send")
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
