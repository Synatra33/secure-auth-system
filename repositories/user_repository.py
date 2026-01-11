from typing import Protocol, Iterable, Optional

from domain.user import User


class UserRepository(Protocol):
    """
    Storage abstraction for User entities.
    No business logic allowed.
    """

    def get_by_username(self, username: str) -> Optional[User]:
        ...

    def save(self, user: User) -> None:
        ...

    def delete(self, username: str) -> None:
        ...

    def exists(self, username: str) -> bool:
        ...

    def list_all(self) -> Iterable[User]:
        ...
