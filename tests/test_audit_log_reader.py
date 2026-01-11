import json
from pathlib import Path

from security.audit_logger import AuditLogger
from security.audit_events import AuditEventType
from security.audit_log_reader import AuditLogReader



def test_audit_logger_writes_event(tmp_path: Path):
    log_file = tmp_path / "audit.log"
    logger = AuditLogger(log_file)

    logger.log(
        event_type=AuditEventType.LOGIN_FAILURE,
        actor="alice",
        target="alice",
        source="cli",
        metadata={"reason": "invalid_credentials"},
    )

    assert log_file.exists()

    lines = log_file.read_text().strip().splitlines()
    assert len(lines) == 1

    event = json.loads(lines[0])
    assert event["event_type"] == "LOGIN_FAILURE"
    assert event["actor"] == "alice"
    assert event["target"] == "alice"
    assert event["source"] == "cli"
    assert event["metadata"]["reason"] == "invalid_credentials"



def test_read_events_by_user(tmp_path: Path):
    log_file = tmp_path / "audit.log"

    with log_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({
            "event_type": "LOGIN_FAILURE",
            "actor": "alice",
            "target": "alice"
        }) + "\n")
        f.write(json.dumps({
            "event_type": "ROLE_CHANGED",
            "actor": "admin",
            "target": "bob"
        }) + "\n")

    reader = AuditLogReader(log_file)
    events = reader.read_by_user("alice")

    assert len(events) == 1
    assert events[0]["event_type"] == "LOGIN_FAILURE"
