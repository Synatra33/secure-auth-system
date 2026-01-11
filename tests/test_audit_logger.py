import json
from pathlib import Path

from security.audit_logger import AuditLogger
from security.audit_events import AuditEventType


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



