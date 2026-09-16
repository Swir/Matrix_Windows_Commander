from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Risk(StrEnum):
    READ_ONLY = "read_only"
    REPAIR = "repair"
    CHANGE = "change"


@dataclass(frozen=True, slots=True)
class CommandSpec:
    id: str
    category: str
    title: str
    executable: str
    args: tuple[str, ...] = ()
    description_en: str = ""
    description_pl: str = ""
    admin_required: bool = False
    risk: Risk = Risk.READ_ONLY
    timeout_seconds: int = 90

    @property
    def command_line(self) -> str:
        return format_command(self.executable, self.args)


def quote_windows_arg(value: str) -> str:
    if not value:
        return '""'
    if not any(ch.isspace() or ch in '"&|<>^' for ch in value):
        return value
    return '"' + value.replace('"', '\\"') + '"'


def format_command(executable: str, args: tuple[str, ...] | list[str]) -> str:
    return " ".join([quote_windows_arg(executable), *(quote_windows_arg(arg) for arg in args)])
