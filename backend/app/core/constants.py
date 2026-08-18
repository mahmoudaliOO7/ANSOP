"""Constants used throughout the application."""

from enum import Enum


class AuditAction(str, Enum):
    """Audit log action types."""

    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    EXECUTE = "EXECUTE"
    ENRICH = "ENRICH"
    RISK_ASSESS = "RISK_ASSESS"


class Severity(str, Enum):
    """Event severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class DetectionStatus(str, Enum):
    """Detection lifecycle status."""

    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentStatus(str, Enum):
    """Incident lifecycle status."""

    NEW = "NEW"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    CONTAINMENT = "CONTAINMENT"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class ApprovalStatus(str, Enum):
    """Approval request status."""

    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    EXECUTING = "EXECUTING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ResponseStatus(str, Enum):
    """Response action status."""

    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class DeviceType(str, Enum):
    """Network device types."""

    FIREWALL = "FIREWALL"
    ROUTER = "ROUTER"
    IDS = "IDS"
    IDS_IPS = "IDS_IPS"
    SWITCH = "SWITCH"
    PROXY = "PROXY"
    SIMULATOR = "SIMULATOR"
