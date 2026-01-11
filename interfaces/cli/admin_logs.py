from pathlib import Path

from security.audit_log_reader import AuditLogReader
from security.audit_events import AuditEventType
from security.audit_logger import AuditLogger


def view_audit_logs(identity):
    """
    Admin-only audit log viewer (read-only)'
    """


    audit_logger = AuditLogger(Path("storage/audit.log"))
    audit_logger.log(
        AuditEventType.AUDIT_LOG_ACCESSED,
        actor=identity.username,
        source='cli',
    )
    reader = AuditLogReader(Path("storage/audit.log"))

    print("\n=== AUDIT LOG VIEWER ===")
    print("1. View recent events")
    print("2. View events by user")
    print("3. View events by type")
    print("4. Back")

    choice = input("Select option: ").strip()

    if choice == "1":
        events = reader.read_recent()
    elif choice == "2":
        username = input("Username: ").strip()
        events = reader.read_by_user(username)
    elif choice == "3":
        print("Available event types:")
        for e in AuditEventType:
            print("-", e.name)
        name = input("Event type: ").strip().upper()
        events = reader.read_by_event_type(AuditEventType[name])
    else:
        return

    _display(events)


def _display(events: list[dict]) -> None:
    if not events:
        print("No events found.")
        return

    for e in events:
        print(
            f"[{e['timestamp']}] "
            f"{e['event_type']} | "
            f"actor={e['actor']} | "
            f"target={e['target']} | "
            f"{e['metadata']}"
        )
