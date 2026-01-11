from pathlib import Path

from repositories.json_user_repository import JsonUserRepository
from services.auth_service import AuthService
from services.user_service import UserService
from interfaces.cli.login import login_flow
from interfaces.cli.router import route_user
from domain.audit import AuditEvent
from datetime import datetime


class FileAuditLogger:
    def __init__(self, path: Path):
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: AuditEvent) -> None:
        record = {
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type,
            "actor": event.actor,
            "target": event.target,
            "metadata": event.metadata,
        }

        with self._path.open("a", encoding="utf-8") as f:
            f.write(str(record) + "\n")


class InMemoryRefreshTokenRepository:
    def __init__(self):
        self._tokens = {}

    def save(self, record):
        self._tokens[record.token_hash] = record

    def get(self, token_hash):
        return self._tokens.get(token_hash)

    def delete(self, token_hash):
        self._tokens.pop(token_hash, None)

    def delete_all_for_user(self, username):
        self._tokens = {
            k: v for k, v in self._tokens.items() if v.username != username
        }


def main():
    user_repo = JsonUserRepository(Path("storage/users.json"))
    refresh_repo = InMemoryRefreshTokenRepository()
    audit_logger = FileAuditLogger(Path("storage/audit.log"))

    auth_service = AuthService(user_repo, refresh_repo, audit_logger)
    user_service = UserService(user_repo, auth_service, audit_logger)

    login_flow(auth_service, user_service)


if __name__ == "__main__":
    main()
