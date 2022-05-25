# coding=utf-8
import getopt
import logging
import sys
from typing import Any

from .cmd import CmdWrapper
from .log import logger
from .pet import PetWrapper
from .rofi import RofiWrapper

VERSION = "0.0.1"


def check_dependency(cmd: str) -> bool:
    try:
        logger.debug("Checking dependency %r", cmd)
        CmdWrapper.run_cmd(["which", cmd])
    except RuntimeError:
        logger.error("%s is not installed on your system.", cmd)
        sys.exit(1)

    return True


def parse_args() -> dict[str, bool]:
    parsed_args = {
        "debug": False,
        "notify": False,
        "terminal": False,
    }
    logger.info(sys.argv[1:])
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "dnt", ["debug", "notify", "terminal"])
    except getopt.GetoptError as exc:
        logger.critical("Error while parsing arguments: %s", exc)
        sys.exit(1)

    for opt, _ in opts:
        if opt in ("-n", "--notify"):
            parsed_args["notify"] = True
        elif opt in ("-d", "--debug"):
            parsed_args["debug"] = True
        elif opt in ("-t", "--terminal"):
            parsed_args["terminal"] = True
        else:
            logger.warning("Unhandled option %r.", opt)

    return parsed_args


def run(**args: Any) -> None:
    if args["debug"]:
        logger.setLevel(logging.DEBUG)
        for arg, val in args.items():
            logger.debug("Argument %s=%s", arg, val)

    check_dependency("pet")
    check_dependency("wl-copy")
    if args["notify"]:
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
        CmdWrapper.run_detached_cmd(
            ["wl-copy", info],
        )
        if args["notify"]:
            CmdWrapper.run_detached_cmd(["notify-send", "Snippet copied"])
        if args["terminal"]:
            CmdWrapper.run_detached_cmd(["alacritty", "--class", "scratchpad"])


def main() -> None:
    script_args = parse_args()
    run(**script_args)


if __name__ == "__main__":
    main()
