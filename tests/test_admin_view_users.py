from datetime import datetime
from pathlib import Path

from repositories.json_user_repository import JsonUserRepository
from services.user_service import UserService
from domain.user import User, UserStatus
from domain.role import Role


def test_admin_can_list_users(tmp_path: Path):
    repo = JsonUserRepository(tmp_path / "users.json")
    service = UserService(repo)

    user1 = User(
        username="alice",
        role=Role.USER,
        status=UserStatus.ACTIVE,
        password_hash="h",
        password_salt="s",
        failed_attempts=0,
        locked_until=None,
        created_at=datetime.utcnow(),
    )

    user2 = User(
        username="admin",
        role=Role.ADMIN,
        status=UserStatus.ACTIVE,
        password_hash="h",
        password_salt="s",
        failed_attempts=0,
        locked_until=None,
        created_at=datetime.utcnow(),
    )

    repo.save(user1)
    repo.save(user2)

    users = service.list_users()
    usernames = {u.username for u in users}

    assert usernames == {"alice", "admin"}
