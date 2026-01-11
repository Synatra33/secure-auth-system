import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from security.audit_events import AuditEventType


class AuditLogger:
    def __init__(self, log_file: Path):
        self._log_file = log_file
        self._log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        event_type: AuditEventType,
        actor: str,
        target: Optional[str] = None,
        source: str = "system",
        metadata: Optional[dict] = None,
    ) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type.name,
            "actor": actor,
            "target": target or actor,
            "source": source,
            "metadata": metadata or {},
        }

        with self._log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
