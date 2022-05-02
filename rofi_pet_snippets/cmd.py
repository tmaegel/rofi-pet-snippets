#!/usr/bin/env python
# coding=utf-8

import subprocess
from typing import Tuple, Union

from .log import logger


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
                    f"Error while running command '{cmd}' [{proc.returncode}]: {err!r}"
                )

        return (
            out.decode("utf-8") if out else None,
            err.decode("utf-8") if err else None,
            proc.returncode if proc else -1,
        )
