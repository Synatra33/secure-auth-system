from pathlib import Path

from security.audit_logger import AuditLogger
from security.audit_events import AuditEventType


def test_admin_audit_log_access_logged(tmp_path: Path):
    log_file = tmp_path / "audit.log"
    logger = AuditLogger(log_file)

    logger.log(
        AuditEventType.AUDIT_LOG_ACCESSED,
        actor="admin",
        source="cli"
    )

    content = log_file.read_text()
    assert "AUDIT_LOG_ACCESSED" in content
    assert "admin" in content
