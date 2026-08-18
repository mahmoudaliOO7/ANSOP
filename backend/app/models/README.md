# Database Models

SQLAlchemy ORM models for ANSOP.

## Overview

ANSOP uses SQLAlchemy 2.0 with the declarative ORM style for database models. All models use UUID primary keys and include timestamp tracking.

## Core Models

### Authentication & Authorization

- **User** — Application users with credentials
- **Role** — Role definitions (ADMIN, SOC_ANALYST, APPROVER, VIEWER)
- **Permission** — Fine-grained permissions
- **UserRole** — User-to-role association
- **RolePermission** — Role-to-permission association

### Detection & Events

- **Detection** — Raw security events from detectors
- **EnrichmentResult** — Enrichment data for detections
- **RiskAssessment** — Risk score and assessment results
- **Event** — Normalized internal event representation

### Rules & Decisions

- **Rule** — Policy rules for decision engine
- **RuleCondition** — Conditions within a rule
- **RuleAction** — Actions triggered by rules
- **RuleExecution** — Execution history and results

### Incidents & Response

- **Incident** — Security incidents (grouped detections)
- **IncidentTimeline** — Incident status changes
- **ApprovalRequest** — Pending approvals for actions
- **ApprovalDecision** — Approval/rejection decisions
- **ResponseAction** — Actions executed in response
- **ResponseResult** — Results of response actions

### Configuration & Devices

- **NetworkDevice** — Lab network devices (firewall, router, etc.)
- **DeviceConnector** — Device connection credentials
- **AllowlistEntry** — IP/domain allowlists
- **DenylistEntry** — IP/domain denylists
- **Configuration** — System configuration key-value pairs

### Audit & Logging

- **AuditLog** — Immutable audit trail
- **AuditLogEntry** — Individual audit events

## Model Relationships

```
User
  ├── many-to-many → Role (via UserRole)
  ├── has-many → AuditLog
  └── has-many → ApprovalDecision

Role
  ├── many-to-many → Permission (via RolePermission)
  └── many-to-many → User (via UserRole)

Detection
  ├── has-one → EnrichmentResult
  ├── has-one → RiskAssessment
  ├── has-many → Incident (reverse: has-many → Detection)
  └── has-many → AuditLog

Incident
  ├── has-many → Detection
  ├── has-many → IncidentTimeline
  ├── has-many → ResponseAction
  └── has-many → ApprovalRequest

Rule
  ├── has-many → RuleCondition
  ├── has-many → RuleAction
  └── has-many → RuleExecution

ApprovalRequest
  ├── has-many → ApprovalDecision
  ├── belongs-to → ResponseAction (optional)
  └── belongs-to → User (requester)

ResponseAction
  ├── has-one → ResponseResult
  ├── belongs-to → Incident
  └── belongs-to → NetworkDevice (target)

NetworkDevice
  ├── has-many → ResponseAction
  └── has-many → AuditLog
```

## Key Design Decisions

1. **UUID Primary Keys** — Better for distributed systems and security
2. **Timestamps** — `created_at`, `updated_at` on all models
3. **Soft Deletes** — `deleted_at` field for audit trail (where applicable)
4. **Indexes** — On commonly queried fields (source_ip, destination_ip, status)
5. **Constraints** — Foreign key constraints with cascading deletes
6. **Audit Fields** — Track who created/modified each record

## Creating Models

Models inherit from a base class that provides timestamps:

```python
from app.models.base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime

class ExampleModel(Base):
    __tablename__ = "example_table"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
```

## Migrations

Use Alembic for schema migrations:

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Best Practices

1. **Type Hints** — All columns have type hints
2. **Validation** — Use Pydantic schemas for input validation
3. **Relationships** — Define relationships in both directions when needed
4. **Indexes** — Add indexes for query performance
5. **Foreign Keys** — Use cascade delete cautiously
6. **Constraints** — Use unique constraints where appropriate

---

**Phase**: 2 (Database Models & Migrations)  
**Status**: In Development
