"""Pydantic schemas for detection intake API."""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from ipaddress import ip_address, AddressValueError


class DetectionCreateRequest(BaseModel):
    """Detection intake request schema for ingesting security events."""

    # Source information
    source: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Source system (e.g., suricata, snort, syslog, custom_api)",
    )
    detection_id: Optional[str] = Field(
        None,
        max_length=512,
        description="External detection ID from source system",
    )

    # Timestamp (when event occurred)
    timestamp: datetime = Field(
        ...,
        description="When the security event occurred (ISO 8601 format)",
    )

    # Network information (required)
    source_ip: str = Field(
        ...,
        min_length=7,
        max_length=45,
        description="Source IP address (IPv4 or IPv6)",
    )
    source_port: Optional[int] = Field(
        None,
        ge=1,
        le=65535,
        description="Source port number (1-65535)",
    )
    destination_ip: str = Field(
        ...,
        min_length=7,
        max_length=45,
        description="Destination IP address (IPv4 or IPv6)",
    )
    destination_port: Optional[int] = Field(
        None,
        ge=1,
        le=65535,
        description="Destination port number (1-65535)",
    )
    protocol: Optional[str] = Field(
        None,
        max_length=20,
        description="Protocol (tcp, udp, icmp, etc.)",
    )

    # Event classification
    event_type: str = Field(
        "unknown",
        description="Type of security event",
    )
    signature: Optional[str] = Field(
        None,
        max_length=1024,
        description="IDS/IPS signature or rule name",
    )
    description: Optional[str] = Field(
        None,
        description="Human-readable description",
    )

    # Severity (required, but has default)
    severity: str = Field(
        "medium",
        description="Severity level (critical, high, medium, low, info)",
    )

    # Raw data and metadata
    raw_event: Optional[str] = Field(
        None,
        description="Raw event data from source",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Flexible metadata dictionary (sensor name, etc.)",
    )

    @field_validator("source_ip", "destination_ip", mode="before")
    @classmethod
    def validate_ips(cls, v: str) -> str:
        """Validate IP addresses are well-formed."""
        if v is None:
            return v
        try:
            ip_address(v)
        except (ValueError, AddressValueError):
            raise ValueError(f"Invalid IP address: {v}")
        return v

    @field_validator("event_type", "severity", mode="before")
    @classmethod
    def lowercase_enums(cls, v: str) -> str:
        """Convert enum strings to lowercase."""
        if v is None:
            return v
        return str(v).lower()

    @model_validator(mode="after")
    def validate_timestamp_not_future(self) -> "DetectionCreateRequest":
        """Ensure timestamp is not in the future (with 5 minute tolerance for clock skew)."""
        from datetime import timezone, timedelta
        now = datetime.now(timezone.utc)
        if self.timestamp > now + timedelta(minutes=5):
            raise ValueError("Event timestamp cannot be in the future")
        return self

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "source": "suricata",
                "detection_id": "alert-12345",
                "timestamp": "2025-08-18T10:30:45Z",
                "source_ip": "192.168.1.100",
                "source_port": 54321,
                "destination_ip": "10.0.0.50",
                "destination_port": 443,
                "protocol": "tcp",
                "event_type": "suspicious_connection",
                "signature": "ET MALWARE Possible Cryptominer Connection",
                "description": "Possible cryptominer connection attempt detected",
                "severity": "high",
                "raw_event": "...",
                "metadata": {
                    "sensor": "lab-ids-01",
                    "interface": "eth0",
                },
            }
        }


class DetectionListFilter(BaseModel):
    """Query filter schema for listing detections."""

    source: Optional[str] = Field(None, description="Filter by source")
    severity: Optional[str] = Field(None, description="Filter by severity")
    event_type: Optional[str] = Field(None, description="Filter by event type")
    status: Optional[str] = Field(None, description="Filter by status")
    source_ip: Optional[str] = Field(None, description="Filter by source IP")
    destination_ip: Optional[str] = Field(None, description="Filter by destination IP")
    min_score: Optional[float] = Field(None, ge=0, le=100, description="Minimum risk score")
    max_score: Optional[float] = Field(None, ge=0, le=100, description="Maximum risk score")
    start_time: Optional[datetime] = Field(None, description="Start of time range")
    end_time: Optional[datetime] = Field(None, description="End of time range")


class DetectionResponse(BaseModel):
    """Detection response schema for API responses."""

    id: uuid.UUID
    source: str
    detection_id: Optional[str]
    event_timestamp: datetime
    source_ip: str
    source_port: Optional[int]
    destination_ip: str
    destination_port: Optional[int]
    protocol: Optional[str]
    event_type: str
    signature: Optional[str]
    description: Optional[str]
    severity: str
    risk_score: Optional[float]
    confidence: Optional[float]
    status: str
    enrichment_data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class DetectionDetailResponse(DetectionResponse):
    """Detailed detection response with raw event data."""

    raw_event: Optional[str]
    metadata: Optional[Dict[str, Any]]


class BulkDetectionCreateRequest(BaseModel):
    """Request schema for bulk detection ingestion."""

    detections: list[DetectionCreateRequest] = Field(
        ...,
        min_items=1,
        max_items=1000,
        description="List of detections to ingest",
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "detections": [
                    {
                        "source": "suricata",
                        "timestamp": "2025-08-18T10:30:45Z",
                        "source_ip": "192.168.1.100",
                        "destination_ip": "10.0.0.50",
                        "destination_port": 443,
                        "protocol": "tcp",
                        "event_type": "suspicious_connection",
                        "severity": "high",
                    }
                ]
            }
        }


class BulkDetectionResponse(BaseModel):
    """Response for bulk detection ingestion."""

    total: int = Field(..., description="Total detections submitted")
    created: int = Field(..., description="Number of detections created")
    failed: int = Field(..., description="Number of detections that failed")
    errors: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="Details of failed detections",
    )


class DetectionStatsResponse(BaseModel):
    """Detection statistics response."""

    total_count: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    by_source: Dict[str, int]
    avg_risk_score: float
    last_detection_time: Optional[datetime]
