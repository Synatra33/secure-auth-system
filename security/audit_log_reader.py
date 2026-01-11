import json
from pathlib import Path
from typing import Iterable

from security.audit_events import AuditEventType


class AuditLogReader:
    def __init__(self, log_file: Path):
        self._log_file = log_file

    def _read_lines(self) -> Iterable[dict]:
        if not self._log_file.exists():
            return []

        with self._log_file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue

    def read_recent(self, limit: int = 20) -> list[dict]:
        return list(self._read_lines())[-limit:]

    def read_by_user(self, username: str) -> list[dict]:
        return [
            e for e in self._read_lines()
            if e.get("actor") == username or e.get("target") == username
        ]

    def read_by_event_type(self, event_type: AuditEventType) -> list[dict]:
        return [
            e for e in self._read_lines()
            if e.get("event_type") == event_type.name
        ]
