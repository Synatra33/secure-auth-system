from typing import Protocol, Optional
from domain.identity import Identity
from datetime import datetime


class RefreshTokenRecord:
    def __init__(self, token_hash: str, username: str, expires_at: datetime):
        self.token_hash = token_hash
        self.username = username
        self.expires_at = expires_at


class RefreshTokenRepository(Protocol):
    def save(self, record: RefreshTokenRecord) -> None: ...
    def get(self, token_hash: str) -> Optional[RefreshTokenRecord]: ...
    def delete(self, token_hash: str) -> None: ...
    def delete_all_for_user(self, username: str) -> None: ...
