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


# Default roles and their descriptions
DEFAULT_ROLES = {
    "ADMIN": {
        "description": "Full system administration access",
        "permissions": ["*:*"],  # All permissions
    },
    "SOC_ANALYST": {
        "description": "Security operations analyst",
        "permissions": [
            "detection:read",
            "detection:create",
            "incident:read",
            "incident:create",
            "incident:update",
            "approval:read",
            "response:read",
            "audit:read",
        ],
    },
    "APPROVER": {
        "description": "Approval authority for high-impact actions",
        "permissions": [
            "detection:read",
            "incident:read",
            "approval:read",
            "approval:update",
            "response:read",
            "audit:read",
        ],
    },
    "VIEWER": {
        "description": "Read-only access to system",
        "permissions": [
            "detection:read",
            "incident:read",
            "approval:read",
            "response:read",
            "audit:read",
            "rule:read",
            "device:read",
        ],
    },
}

# Default permissions
DEFAULT_PERMISSIONS = [
    # Detection permissions
    {"resource": "detection", "action": "create"},
    {"resource": "detection", "action": "read"},
    {"resource": "detection", "action": "update"},
    {"resource": "detection", "action": "delete"},
    # Incident permissions
    {"resource": "incident", "action": "create"},
    {"resource": "incident", "action": "read"},
    {"resource": "incident", "action": "update"},
    {"resource": "incident", "action": "delete"},
    # Approval permissions
    {"resource": "approval", "action": "read"},
    {"resource": "approval", "action": "update"},
    # Response permissions
    {"resource": "response", "action": "read"},
    {"resource": "response", "action": "create"},
    {"resource": "response", "action": "execute"},
    # Rule permissions
    {"resource": "rule", "action": "read"},
    {"resource": "rule", "action": "create"},
    {"resource": "rule", "action": "update"},
    {"resource": "rule", "action": "delete"},
    # Device permissions
    {"resource": "device", "action": "read"},
    {"resource": "device", "action": "create"},
    {"resource": "device", "action": "update"},
    # Audit permissions
    {"resource": "audit", "action": "read"},
    # User permissions
    {"resource": "user", "action": "create"},
    {"resource": "user", "action": "read"},
    {"resource": "user", "action": "update"},
    {"resource": "user", "action": "delete"},
    # Admin permissions
    {"resource": "admin", "action": "*"},
]
