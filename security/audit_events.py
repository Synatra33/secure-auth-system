from enum import Enum, auto

class AuditEventType(Enum):
    LOGIN_SUCCESS = auto()
    LOGIN_FAILURE = auto()
    LOGOUT = auto()

    ACCOUNT_LOCKED = auto()
    ACCOUNT_UNLOCKED = auto()
    ACCOUNT_SUSPENDED = auto()
    ACCOUNT_REACTIVATED = auto()

    SESSION_CREATED = auto()
    SESSION_EXPIRED = auto()
    REFRESH_TOKEN_USED = auto()

    USER_CREATED = auto()
    USER_DELETED = auto()

    ROLE_CHANGED = auto()

    ADMIN_ACTION = auto()
    AUDIT_LOG_ACCESSED = auto()
