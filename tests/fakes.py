from datetime import datetime
from typing import Optional

from domain.user import User
from repositories.user_repository import UserRepository
from repositories.refresh_token_repository import RefreshTokenRecord


class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users: dict[str, User] = {}

    def get_by_username(self, username: str) -> Optional[User]:
        return self.users.get(username)

    def save(self, user: User) -> None:
        self.users[user.username] = user

    def delete(self, username: str) -> None:
        self.users.pop(username, None)

    def exists(self, username: str) -> bool:
        return username in self.users

    def list_all(self):
        return list(self.users.values())


class FakeRefreshTokenRepository:
    def __init__(self):
        self.tokens: dict[str, RefreshTokenRecord] = {}

    def save(self, record: RefreshTokenRecord) -> None:
        self.tokens[record.token_hash] = record

    def get(self, token_hash: str) -> Optional[RefreshTokenRecord]:
        return self.tokens.get(token_hash)

    def delete(self, token_hash: str) -> None:
        self.tokens.pop(token_hash, None)

    def delete_all_for_user(self, username: str) -> None:
        self.tokens = {
            k: v for k, v in self.tokens.items() if v.username != username
        }


class FakeAuditLogger:
    def __init__(self):
        self.events = []

    def log(self, event):
        self.events.append(event)
