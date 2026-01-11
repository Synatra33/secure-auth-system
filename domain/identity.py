from dataclasses import dataclass
from datetime import datetime


from domain.role import Role




@dataclass(frozen=True)
class Identity:
    username: str
    role: Role
    issued_at: datetime
    expires_at: datetime



    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.utcnow()
        return now >= self.expires_at
    