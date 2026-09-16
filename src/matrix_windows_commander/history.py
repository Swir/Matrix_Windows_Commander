from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from platformdirs import user_data_dir


@dataclass(slots=True)
class HistoryEntry:
    command_id: str
    title: str
    exit_code: int
    started_at: str
    duration_ms: int


class HistoryStore:
    def __init__(self, limit: int = 100) -> None:
        self.limit = limit
        self.path = Path(user_data_dir("MatrixWindowsCommander", "Swir")) / "history.json"

    def load(self) -> list[HistoryEntry]:
        if not self.path.exists():
            return []
        try:
            values = json.loads(self.path.read_text(encoding="utf-8"))
            return [HistoryEntry(**item) for item in values if isinstance(item, dict)][-self.limit:]
        except Exception:
            return []

    def append(self, entry: HistoryEntry) -> None:
        values = self.load(); values.append(entry); values = values[-self.limit:]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps([asdict(item) for item in values], indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
