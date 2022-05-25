# coding=utf-8
from subprocess import DEVNULL, PIPE, Popen
from typing import Optional, Tuple

from .log import logger


class CmdWrapper:
    @staticmethod
    def run_cmd(
        cmd: list[str], pipe: bool = True
    ) -> Tuple[Optional[str], Optional[str], int]:
        out = None
        err = None
        proc = None
        try:
            with Popen(
                cmd,
                stdout=PIPE if pipe else DEVNULL,
                stderr=PIPE if pipe else DEVNULL,
                # stdin=PIPE if pipe else DEVNULL,
            ) as proc:
                out, err = proc.communicate()
        except (OSError, ValueError, FileNotFoundError) as exc:
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
                    f"Error while running command '{cmd}' [{proc.returncode}]: {err!r}"
                )

        return (
            out.decode("utf-8") if out else None,
            err.decode("utf-8") if err else None,
            proc.returncode if proc else -1,
        )

    @staticmethod
    def run_detached_cmd(cmd: list[str]) -> None:
        try:
            with Popen(
                cmd,
                stdout=DEVNULL,
                stderr=DEVNULL,
                stdin=DEVNULL,
            ):
                pass
        except (OSError, ValueError, FileNotFoundError) as exc:
            logger.critical("Error while running command '%s': %s", cmd, exc)
            raise RuntimeError(f"Error while running command '{cmd}': {exc}") from exc
