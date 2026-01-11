import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple

from domain.identity import Identity
from domain.user import UserStatus
from security.password_hasher import PasswordHasher
from repositories.user_repository import UserRepository
from repositories.refresh_token_repository import (
    RefreshTokenRepository,
    RefreshTokenRecord,
)
from domain.audit import AuditEvent


class AuthService:
    MAX_ATTEMPTS = 5
    LOCK_DURATION = timedelta(minutes=15)
    SESSION_DURATION = timedelta(minutes=30)
    REFRESH_DURATION = timedelta(days=7)

    def __init__(
        self,
        user_repo: UserRepository,
        refresh_repo: RefreshTokenRepository,
        audit_logger,
    ):
        self._users = user_repo
        self._refresh = refresh_repo
        self._audit = audit_logger

    # -------- AUTHENTICATION --------

    def authenticate(
        self, username: str, password: str
    ) -> Optional[Tuple[Identity, str]]:
        user = self._users.get_by_username(username)
        now = datetime.utcnow()

        # uniform failure
        if not user or user.status != UserStatus.ACTIVE:
            self._audit.log(
                AuditEvent(now, "LOGIN_FAILURE", None, username, {})
            )
            return None

        if user.locked_until and user.locked_until > now:
            self._audit.log(
                AuditEvent(now, "LOGIN_BLOCKED_LOCKED", None, username, {})
            )
            return None

        if not PasswordHasher.verify(
            password, user.password_salt, user.password_hash
        ):
            user.failed_attempts += 1

            if user.failed_attempts >= self.MAX_ATTEMPTS:
                user.locked_until = now + self.LOCK_DURATION
                user.failed_attempts = 0
                self._audit.log(
                    AuditEvent(now, "ACCOUNT_LOCKED", None, username, {})
                )
            else:
                self._audit.log(
                    AuditEvent(now, "LOGIN_FAILURE", None, username, {})
                )

            self._users.save(user)
            return None

        # SUCCESS
        user.failed_attempts = 0
        user.locked_until = None
        self._users.save(user)

        identity = Identity(
            username=user.username,
            role=user.role,
            issued_at=now,
            expires_at=now + self.SESSION_DURATION,
        )

        refresh_token = self._issue_refresh_token(user.username)

        self._audit.log(
            AuditEvent(
                now,
                "LOGIN_SUCCESS",
                user.username,
                user.username,
                {"expires_at": identity.expires_at.isoformat()},
            )
        )

        return identity, refresh_token

    # -------- SESSION REFRESH --------

    def refresh_session(
        self, refresh_token: str
    ) -> Optional[Tuple[Identity, str]]:
        now = datetime.utcnow()
        token_hash = self._hash_token(refresh_token)

        record = self._refresh.get(token_hash)
        if not record or record.expires_at <= now:
            return None

        user = self._users.get_by_username(record.username)
        if not user or user.status != UserStatus.ACTIVE:
            return None

        # rotate token
        self._refresh.delete(token_hash)

        identity = Identity(
            username=user.username,
            role=user.role,
            issued_at=now,
            expires_at=now + self.SESSION_DURATION,
        )

        new_refresh = self._issue_refresh_token(user.username)

        self._audit.log(
            AuditEvent(
                now,
                "SESSION_REFRESH",
                user.username,
                user.username,
                {},
            )
        )

        return identity, new_refresh

    # -------- LOGOUT / INVALIDATION --------

    def invalidate_all_sessions(self, username: str) -> None:
        self._refresh.delete_all_for_user(username)

    # -------- INTERNAL HELPERS --------

    def _issue_refresh_token(self, username: str) -> str:
        raw = secrets.token_urlsafe(32)
        token_hash = self._hash_token(raw)

        record = RefreshTokenRecord(
            token_hash=token_hash,
            username=username,
            expires_at=datetime.utcnow() + self.REFRESH_DURATION,
        )

        self._refresh.save(record)
        return raw

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
