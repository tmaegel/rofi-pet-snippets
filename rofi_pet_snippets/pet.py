# coding=utf-8
import re
from typing import TypedDict

from .cmd import CmdWrapper


class Snippet(TypedDict):
    description: str
    command: str
    tags: list[str]


class PetWrapper(CmdWrapper):
    @classmethod
    def list_snippets(cls) -> list[Snippet]:
        def reset_snippet() -> Snippet:
            return {
                "description": "",
                "command": "",
                "tags": [],
            }

        snippet = reset_snippet()
        snippets: list[Snippet] = []
        out, _, _ = cls.run_cmd(["pet", "list"])
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
