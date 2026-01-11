from datetime import datetime

from domain.role import Role
from domain.user import User, UserStatus
from domain.identity import Identity
from domain.audit import AuditEvent
from security.password_hasher import PasswordHasher
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository, auth_service, audit_logger):
        self._users = user_repo
        self._auth = auth_service
        self._audit = audit_logger

    # ---------- INTERNAL GUARDS ----------

    @staticmethod
    def _require_valid_identity(identity: Identity) -> None:
        if identity.is_expired():
            raise PermissionError("Session expired")

    @staticmethod
    def _require_admin(identity: Identity) -> None:
        if identity.role != Role.ADMIN:
            raise PermissionError("Admin privileges required")

    # ---------- USER CREATION ----------

    def create_user(self, username: str, password: str, role: Role) -> User:
        if self._users.exists(username):
            raise ValueError("User already exists")

        salt, hash_ = PasswordHasher.hash_password(password)

        user = User(
            username=username,
            role=role,
            status=UserStatus.ACTIVE,
            password_hash=hash_,
            password_salt=salt,
            failed_attempts=0,
            locked_until=None,
            created_at=datetime.utcnow(),
        )

        self._users.save(user)

        self._audit.log(
            AuditEvent(
                datetime.utcnow(),
                "USER_CREATED",
                None,
                username,
                {"role": role.value},
            )
        )

        return user

    # ---------- ROLE MANAGEMENT ----------

    def change_role(
        self, target_username: str, new_role: Role, actor: Identity
    ) -> None:
        self._require_valid_identity(actor)
        self._require_admin(actor)

        user = self._users.get_by_username(target_username)
        if not user:
            raise ValueError("User not found")

        # invariant: must retain at least one admin
        if user.role == Role.ADMIN and new_role != Role.ADMIN:
            admins = [
                u for u in self._users.list_all() if u.role == Role.ADMIN
            ]
            if len(admins) <= 1:
                raise RuntimeError("System must retain at least one admin")

        user.role = new_role
        self._users.save(user)

        # invalidate sessions
        self._auth.invalidate_all_sessions(target_username)

        self._audit.log(
            AuditEvent(
                datetime.utcnow(),
                "ROLE_CHANGED",
                actor.username,
                target_username,
                {"new_role": new_role.value},
            )
        )

    # ---------- ACCOUNT STATUS ----------

    def suspend_user(self, target_username: str, actor: Identity) -> None:
        self._require_valid_identity(actor)
        self._require_admin(actor)

        user = self._users.get_by_username(target_username)
        if not user:
            raise ValueError("User not found")

        user.status = UserStatus.SUSPENDED
        self._users.save(user)

        self._auth.invalidate_all_sessions(target_username)

        self._audit.log(
            AuditEvent(
                datetime.utcnow(),
                "USER_SUSPENDED",
                actor.username,
                target_username,
                {},
            )
        )

    def unlock_user(self, target_username: str, actor: Identity) -> None:
        self._require_valid_identity(actor)
        self._require_admin(actor)

        user = self._users.get_by_username(target_username)
        if not user:
            raise ValueError("User not found")

        user.status = UserStatus.ACTIVE
        user.failed_attempts = 0
        user.locked_until = None

        self._users.save(user)

        self._audit.log(
            AuditEvent(
                datetime.utcnow(),
                "USER_UNLOCKED",
                actor.username,
                target_username,
                {},
            )
        )

    # ---------- DELETION ----------

    def delete_user(self, target_username: str, actor: Identity) -> None:
        self._require_valid_identity(actor)
        self._require_admin(actor)

        user = self._users.get_by_username(target_username)
        if not user:
            return

        if user.role == Role.ADMIN:
            admins = [
                u for u in self._users.list_all() if u.role == Role.ADMIN
            ]
            if len(admins) <= 1:
                raise RuntimeError("System must retain at least one admin")

        self._users.delete(target_username)
        self._auth.invalidate_all_sessions(target_username)

        self._audit.log(
            AuditEvent(
                datetime.utcnow(),
                "USER_DELETED",
                actor.username,
                target_username,
                {},
            )
        )
