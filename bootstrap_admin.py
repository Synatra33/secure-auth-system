from pathlib import Path
from datetime import datetime

from repositories.json_user_repository import JsonUserRepository
from domain.user import User, UserStatus
from domain.role import Role
from security.password_hasher import PasswordHasher

from getpass import getpass




def main():
    repo = JsonUserRepository(Path("storage/users.json"))

    if list(repo.list_all()):
        print("Users already exist. Bootstrap skipped.")
        return

    print("=== ADMIN BOOTSTRAP ===")
    username = input("Admin username: ").strip().lower()
    password = getpass("Admin password: ").strip()

    salt, password_hash = PasswordHasher.hash_password(password)

    admin = User(
        username=username,
        role=Role.ADMIN,
        status=UserStatus.ACTIVE,
        password_hash=password_hash,
        password_salt=salt,
        failed_attempts=0,
        locked_until=None,
        created_at=datetime.utcnow(),
    )

    repo.save(admin)
    print("Admin created successfully.")


if __name__ == "__main__":
    main()
