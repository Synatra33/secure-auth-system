from datetime import datetime, timedelta

from services.auth_service import AuthService
from domain.user import User, UserStatus
from domain.role import Role
from security.password_hasher import PasswordHasher
from tests.fakes import (
    FakeUserRepository,
    FakeRefreshTokenRepository,
    FakeAuditLogger,
)


def setup_auth():
    users = FakeUserRepository()
    refresh = FakeRefreshTokenRepository()
    audit = FakeAuditLogger()
    auth = AuthService(users, refresh, audit)
    return users, refresh, audit, auth


def create_user(users, username, password, role=Role.USER):
    salt, hash_ = PasswordHasher.hash_password(password)
    users.save(
        User(
            username=username,
            role=role,
            status=UserStatus.ACTIVE,
            password_hash=hash_,
            password_salt=salt,
            failed_attempts=0,
            locked_until=None,
            created_at=datetime.utcnow(),
        )
    )


def test_successful_login():
    users, _, _, auth = setup_auth()
    create_user(users, "alice", "Pass123")

    result = auth.authenticate("alice", "Pass123")
    assert result is not None

    identity, refresh = result
    assert identity.username == "alice"
    assert refresh


def test_failed_login_increments_attempts():
    users, _, _, auth = setup_auth()
    create_user(users, "bob", "Correct123")

    for _ in range(4):
        assert auth.authenticate("bob", "wrong") is None

    user = users.get_by_username("bob")
    assert user.failed_attempts == 4


def test_account_locks_after_max_attempts():
    users, _, _, auth = setup_auth()
    create_user(users, "carol", "Correct123")

    for _ in range(auth.MAX_ATTEMPTS):
        auth.authenticate("carol", "wrong")

    user = users.get_by_username("carol")
    assert user.locked_until is not None


def test_locked_account_cannot_login():
    users, _, _, auth = setup_auth()
    create_user(users, "dan", "Correct123")

    for _ in range(auth.MAX_ATTEMPTS):
        auth.authenticate("dan", "wrong")

    assert auth.authenticate("dan", "Correct123") is None
