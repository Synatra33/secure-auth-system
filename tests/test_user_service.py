from datetime import datetime

import pytest

from services.user_service import UserService
from domain.identity import Identity
from domain.role import Role
from tests.fakes import (
    FakeUserRepository,
    FakeRefreshTokenRepository,
    FakeAuditLogger,
)
from services.auth_service import AuthService


def setup_services():
    users = FakeUserRepository()
    refresh = FakeRefreshTokenRepository()
    audit = FakeAuditLogger()
    auth = AuthService(users, refresh, audit)
    service = UserService(users, auth, audit)
    return users, auth, service


def admin_identity():
    return Identity(
        username="admin",
        role=Role.ADMIN,
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow().replace(year=2099),
    )


def test_cannot_delete_last_admin():
    users, auth, service = setup_services()

    service.create_user("admin", "AdminPass123", Role.ADMIN)
    identity = admin_identity()

    with pytest.raises(RuntimeError):
        service.delete_user("admin", identity)


def test_non_admin_cannot_change_role():
    users, auth, service = setup_services()

    service.create_user("admin", "AdminPass123", Role.ADMIN)
    service.create_user("bob", "UserPass123", Role.USER)

    non_admin = Identity(
        username="bob",
        role=Role.USER,
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow().replace(year=2099),
    )

    with pytest.raises(PermissionError):
        service.change_role("admin", Role.USER, non_admin)
