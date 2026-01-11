from dataclasses import dataclass
from datetime import datetime



@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    event_type: str
    actor: str | None
    target: str | None
    metadata: dict