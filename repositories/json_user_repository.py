import json
from pathlib import Path
from datetime import datetime
from typing import Iterable, Optional

from domain.user import User, UserStatus
from domain.role import Role
from repositories.user_repository import UserRepository


class JsonUserRepository(UserRepository):
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_raw(self) -> dict:
        if not self._file_path.exists():
            return {}

        try:
            content = self._file_path.read_text(encoding="utf-8")
            return json.loads(content) if content else {}
        except json.JSONDecodeError:
            raise RuntimeError("User storage corrupted")

    def _save_raw(self, data: dict) -> None:
        self._file_path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    def get_by_username(self, username: str) -> Optional[User]:
        data = self._load_raw()
        record = data.get(username)

        if not record:
            return None

        return User(
            username=username,
            role=Role(record["role"]),
            status=UserStatus(record["status"]),
            password_hash=record["password_hash"],
            password_salt=record["password_salt"],
            failed_attempts=record["failed_attempts"],
            locked_until=(
                datetime.fromisoformat(record["locked_until"])
                if record["locked_until"]
                else None
            ),
            created_at=datetime.fromisoformat(record["created_at"]),
        )

    def save(self, user: User) -> None:
        data = self._load_raw()

        data[user.username] = {
            "role": user.role.value,
            "status": user.status.value,
            "password_hash": user.password_hash,
            "password_salt": user.password_salt,
            "failed_attempts": user.failed_attempts,
            "locked_until": (
                user.locked_until.isoformat()
                if user.locked_until
                else None
            ),
            "created_at": user.created_at.isoformat(),
        }

        self._save_raw(data)

    def delete(self, username: str) -> None:
        data = self._load_raw()
        data.pop(username, None)
        self._save_raw(data)

    def exists(self, username: str) -> bool:
        return username in self._load_raw()

    def list_all(self) -> Iterable[User]:
        data = self._load_raw()
        for username in data:
            user = self.get_by_username(username)
            if user:
                yield user
