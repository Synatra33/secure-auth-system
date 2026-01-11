from dataclasses import dataclass
from datetime import datetime
from enum import Enum


from domain.role import Role




class UserStatus(Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    SUSPENDED = "suspended"



@dataclass
class User:
    username: str
    role: Role
    status: UserStatus


    password_hash: str
    password_salt: str


    failed_attempts: int
    locked_until: datetime | None



    created_at: datetime