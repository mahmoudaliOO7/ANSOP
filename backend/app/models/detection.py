"""Detection and event models for security event tracking."""

from sqlalchemy import String, Integer, DateTime, Text, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
import uuid
from app.models.base import Base, TimestampMixin, UUIDMixin


class EventSeverity(str, enum.Enum):
    """Event severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class EventType(str, enum.Enum):
    """Types of security events."""

    SUSPICIOUS_CONNECTION = "suspicious_connection"
    MALWARE_DETECTION = "malware_detection"
    INTRUSION_ATTEMPT = "intrusion_attempt"
    DATA_EXFILTRATION = "data_exfiltration"
    POLICY_VIOLATION = "policy_violation"
    ANOMALOUS_BEHAVIOR = "anomalous_behavior"
    BRUTE_FORCE = "brute_force"
    RECONNAISSANCE = "reconnaissance"
    UNKNOWN = "unknown"


class DetectionStatus(str, enum.Enum):
    """Status of a detection."""

    NEW = "new"
    PROCESSING = "processing"
    ENRICHED = "enriched"
    SCORED = "scored"
    DECIDED = "decided"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    RESPONDED = "responded"
    CLOSED = "closed"


class Detection(Base, UUIDMixin, TimestampMixin):
    """Security event detection model.
    
    Represents a single security event ingested from IDS, logs, or API.
    """

    __tablename__ = "detections"

    # Source and identification
    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Source of detection (e.g., suricata, snort, syslog)",
    )
    detection_id: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="External detection/event ID from source system",
    )

    # Timestamp (when event occurred, not when ingested)
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="When the event actually occurred",
    )

    # Network information
    source_ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True,
        comment="Source IP address (IPv4 or IPv6)",
    )
    source_port: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Source port number",
    )
    destination_ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        index=True,
        comment="Destination IP address (IPv4 or IPv6)",
    )
    destination_port: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Destination port number",
    )
    protocol: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        comment="Protocol (tcp, udp, icmp, etc.)",
    )

    # Event classification
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type"),
        nullable=False,
        index=True,
        comment="Type/category of security event",
    )
    signature: Mapped[str] = mapped_column(
        String(1024),
        nullable=True,
        comment="IDS/IPS signature or rule name",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Human-readable description of the event",
    )

    # Severity and risk
    severity: Mapped[EventSeverity] = mapped_column(
        SQLEnum(EventSeverity, name="event_severity"),
        default=EventSeverity.MEDIUM,
        nullable=False,
        index=True,
        comment="Initial severity from source",
    )
    risk_score: Mapped[float | None] = mapped_column(
        nullable=True,
        comment="Calculated risk score (0-100)",
    )
    confidence: Mapped[float | None] = mapped_column(
        nullable=True,
        comment="Confidence score (0-100)",
    )

    # Raw event and context
    raw_event: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Raw event data from source",
    )
    metadata: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Flexible metadata dictionary from source",
    )

    # Status tracking
    status: Mapped[DetectionStatus] = mapped_column(
        SQLEnum(DetectionStatus, name="detection_status"),
        default=DetectionStatus.NEW,
        nullable=False,
        index=True,
        comment="Current processing status",
    )

    # Enrichment results
    enrichment_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Enrichment results (IP reputation, threat intel, etc.)",
    )

    # Relationships
    # incident_id: Mapped[uuid.UUID | None] = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey("incidents.id"),
    #     nullable=True,
    #     comment="Associated incident if any",
    # )

    __table_args__ = (
        # Composite index for common queries
        Index("ix_detections_source_timestamp", "source", "event_timestamp"),
        Index("ix_detections_ips_timestamp", "source_ip", "destination_ip", "event_timestamp"),
        Index("ix_detections_status_severity", "status", "severity"),
    )

    def __repr__(self) -> str:
        return (
            f"<Detection(id={self.id}, source={self.source}, "
            f"src_ip={self.source_ip}, dst_ip={self.destination_ip}, "
            f"type={self.event_type}, severity={self.severity}, status={self.status})>"
        )
