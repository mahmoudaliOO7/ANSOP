# ANSOP — Automated Network Security Orchestration Platform

A lightweight, professional-grade SOAR-style security orchestration platform built for cybersecurity education and secure laboratory demonstrations.

## 🎯 Overview

ANSOP implements a complete security event pipeline:

```
DETECT → ENRICH → DECIDE → APPROVE → RESPOND → AUDIT
```

Built from scratch using Python, FastAPI, PostgreSQL, and React, ANSOP demonstrates:

- **Detection Intake**: Unified API for security events from IDS, logs, or custom sources
- **Event Normalization**: Standardized internal event schema
- **Threat Intelligence Enrichment**: IP reputation, domain analysis, threat intel integration
- **Risk Scoring**: Transparent, explainable risk calculation engine
- **Decision Engine**: Rule-based policy evaluation with deterministic outcomes
- **Human Approval Workflow**: Mandatory approval gates for impactful actions
- **Response Orchestration**: Simulated and lab-network device integration
- **Incident Management**: Full incident lifecycle tracking
- **Audit Logging**: Immutable operational audit trail
- **Dashboard**: SOC-style operational visibility
- **RBAC**: Role-based access control with backend enforcement

## 🔐 Security by Design

- **Lab-Safe**: All responses restricted to explicitly configured laboratory devices
- **Fail-Closed**: Unknown actions default to reject
- **Transparent Scoring**: No opaque AI-based risk scores; all factors are explainable
- **Approval-Enforced**: High-impact actions require human approval and server-side validation
- **Auditable**: Complete chain-of-custody for every security decision
- **No Offensive Capability**: Cannot be used to attack external systems

---

## 📋 Project Requirements

### Functional Requirements

1. ✅ Detection intake API with validation
2. ✅ Event normalization to internal schema
3. ✅ Modular enrichment engine (IP reputation, threat intelligence)
4. ✅ Transparent risk scoring algorithm
5. ✅ Rule-based decision engine with policies
6. ✅ Human approval workflow with state management
7. ✅ Response orchestration (simulator, firewall, network devices)
8. ✅ Lab network device integration with safety controls
9. ✅ Incident lifecycle management
10. ✅ Dashboard with SOC-style views
11. ✅ Complete audit logging
12. ✅ JWT-based authentication
13. ✅ Role-based access control (ADMIN, SOC_ANALYST, APPROVER, VIEWER)
14. ✅ Configuration management (rules, devices, settings)
15. ✅ OpenAPI documentation
16. ✅ Comprehensive test suite
17. ✅ Docker-based development and deployment
18. ✅ Professional documentation

### Non-Functional Requirements

- Python 3.10+
- PostgreSQL 13+
- TypeScript & React
- Clean modular architecture
- Type hints throughout
- Comprehensive logging with correlation IDs
- Performance suitable for lab demonstrations
- Production-quality security practices

---

## 🏗️ Architecture

### High-Level Component Flow

```
┌─────────────────────┐
│ Detection Sources   │
│ IDS / Logs / API    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Detection Intake    │
│ API / Collector     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Event Normalizer    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Enrichment Engine   │
│ Threat Intel /      │
│ Reputation          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Risk Engine         │
│ Severity + Score    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Decision Engine     │
│ Rules / Policies    │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
 Auto         Approval
 Response      │
    │          │
    │  Human   │
    │  Approval│
    └──────┬───┘
           ▼
┌─────────────────────┐
│ Response Engine     │
│ Firewall / Router   │
│ / Simulator         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Audit Logger        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dashboard           │
│ SOC Visibility      │
└─────────────────────┘
```

### Project Structure

```
ansop/
│
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   ├── core/             # Core config, security, constants
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic services
│   │   ├── engines/          # Core engines
│   │   │   ├── detection/
│   │   │   ├── enrichment/
│   │   │   ├── risk/
│   │   │   ├── decision/
│   │   │   └── response/
│   │   ├── connectors/       # External system connectors
│   │   ├── workers/          # Background tasks
│   │   ├── middleware/       # Request/response middleware
│   │   └── main.py           # Application entry point
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   │
│   ├── alembic/              # Database migrations
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile
│   ├── .dockerignore
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API clients
│   │   ├── hooks/            # Custom React hooks
│   │   ├── types/            # TypeScript types
│   │   ├── styles/           # Global styles
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   │
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .dockerignore
│
├── config/
│   ├── rules/
│   │   ├── example_rules.yaml
│   │   └── README.md
│   ├── devices/
│   │   ├── example_devices.yaml
│   │   └── README.md
│   └── examples/
│       ├── example_detection.json
│       ├── example_rule.json
│       └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── deployment.md
│   ├── testing.md
│   ├── demo-scenario.md
│   ├── database.md
│   ├── security-model.md
│   └── development.md
│
├── docker-compose.yml
├── Makefile
├── .env.example
├── .gitignore
├── .dockerignore
├── SECURITY.md
└── README.md
```

---

## 🛠️ Technology Stack

### Backend

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.109+ |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0+ |
| Migrations | Alembic |
| Database | PostgreSQL 13+ |
| Authentication | Python-JWT, Passlib |
| Code Quality | Ruff, Black, MyPy |
| Testing | Pytest, pytest-asyncio |
| HTTP Client | HTTPX |
| Logging | Python logging with JSON |

### Frontend

| Component | Technology |
|-----------|-----------|
| Framework | React 18+ |
| Language | TypeScript |
| Build Tool | Vite |
| Package Manager | npm |
| State Management | React Context API / Zustand |
| UI Framework | Tailwind CSS + Shadcn/ui |
| API Client | Axios / HTTPX |
| Testing | Vitest, React Testing Library |

### Infrastructure

| Component | Technology |
|-----------|-----------|
| Container | Docker |
| Orchestration | Docker Compose |
| Database | PostgreSQL |
| Secrets | Environment variables (.env) |
| Networking | User-defined bridge networks |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)
- Git

### Development with Docker Compose

1. **Clone and Configure**

   ```bash
   git clone https://github.com/mahmoudaliOO7/ANSOP.git
   cd ANSOP
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start Services**

   ```bash
   docker-compose up --build
   ```

   Services will start:
   - **Backend API**: http://localhost:8000
   - **Frontend**: http://localhost:5173
   - **PostgreSQL**: localhost:5432

3. **Initialize Database**

   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. **Create Admin User**

   ```bash
   docker-compose exec backend python -m app.cli create-admin
   ```

5. **Access the System**

   - Dashboard: http://localhost:5173
   - API Docs: http://localhost:8000/docs
   - Default credentials: `admin` / (check `.env`)

### Local Development

See [Development Guide](docs/development.md) for local setup with virtual environment.

---

## 📡 API Overview

### Core Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /api/v1/auth/login` | Authenticate and receive JWT |
| `POST /api/v1/detections` | Submit security events |
| `GET /api/v1/detections` | List detections with filters |
| `GET /api/v1/detections/{id}` | Retrieve detection details |
| `GET /api/v1/incidents` | List incidents |
| `POST /api/v1/incidents` | Create incident from detection |
| `GET /api/v1/approvals` | List pending approvals |
| `POST /api/v1/approvals/{id}/approve` | Approve pending action |
| `POST /api/v1/approvals/{id}/reject` | Reject pending action |
| `GET /api/v1/audit` | Query audit log |
| `GET /api/v1/dashboard` | Dashboard summary |
| `GET /api/v1/rules` | List active rules |
| `POST /api/v1/rules` | Create new rule |

See [API Documentation](docs/api.md) for complete endpoint reference.

---

## 📥 Detection Example

```bash
curl -X POST http://localhost:8000/api/v1/detections \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "suricata",
    "timestamp": "2025-08-18T10:30:45Z",
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 54321,
    "destination_port": 443,
    "protocol": "tcp",
    "event_type": "suspicious_connection",
    "signature": "ET MALWARE Possible Cryptominer Connection",
    "severity": "medium",
    "raw_event": "...",
    "metadata": {
      "sensor": "lab-ids-01"
    }
  }'
```

---

## 📋 Rule Example

```yaml
# config/rules/example_rules.yaml
version: "1.0"
rules:
  - id: "rule-001"
    name: "Block High-Risk External Connection"
    enabled: true
    priority: 100
    conditions:
      - field: "severity"
        operator: ">="
        value: "high"
      - field: "threat_score"
        operator: ">="
        value: 75
      - field: "source_ip"
        operator: "not_in"
        value: "allowlist:internal_ips"
    actions:
      - type: "BLOCK_IP"
        target: "firewall-lab-01"
        requires_approval: true
    description: "Automatically block external IPs with high threat scores after human approval"
```

See [Configuration Guide](config/) for more examples.

---

## 🔬 Demo Scenario

The platform includes a complete demonstration scenario:

1. Inject a realistic lab-generated detection
2. Watch ANSOP normalize and enrich the event
3. See risk scoring in action
4. Trigger approval workflow
5. Approve and execute simulated response
6. Verify audit trail

See [Demo Scenario](docs/demo-scenario.md) for step-by-step walkthrough.

---

## 🔐 Security Model

ANSOP implements defense-in-depth:

- **Input Validation**: All inputs validated against Pydantic schemas
- **Authentication**: JWT tokens with secure expiry
- **Authorization**: Role-based access control enforced server-side
- **Secrets Management**: No hardcoded credentials; all from environment
- **Lab Safety**: Responses restricted to explicitly configured devices
- **Audit Trail**: Every decision logged with actor, timestamp, action
- **Rate Limiting**: API rate limits prevent abuse
- **CORS**: Restricted cross-origin requests
- **CSRF Protection**: Token-based CSRF prevention
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **Command Injection Prevention**: Command templates, no string concatenation

See [Security Model](docs/security-model.md) for detailed threat analysis.

---

## 📚 Documentation

- [Architecture](docs/architecture.md) — System design and components
- [API Reference](docs/api.md) — Complete endpoint documentation
- [Deployment](docs/deployment.md) — Production deployment guide
- [Testing](docs/testing.md) — Test strategy and execution
- [Demo Scenario](docs/demo-scenario.md) — End-to-end demonstration walkthrough
- [Database Design](docs/database.md) — Data models and relationships
- [Security Model](docs/security-model.md) — Security architecture and threat model
- [Development](docs/development.md) — Local development setup and workflow

---

## 🧪 Testing

ANSOP includes comprehensive tests:

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Run specific test suite
docker-compose exec backend pytest tests/unit/test_risk_engine.py
```

---

## 📊 Dashboard Features

- **Real-time Metrics**: Detection rate, incident count, response status
- **Severity Breakdown**: Visual distribution of event severities
- **Approval Queue**: Pending approvals with details
- **Response History**: Recent automated and manual responses
- **Audit Trail**: Complete operational history
- **Incident Tracking**: Status, severity, related detections
- **Rule Management**: View, enable/disable, edit rules
- **Device Status**: Network device connectivity and health

---

## 🚦 Development Phases

Phase 1 (Current): Repository architecture and foundation
Phase 2: Database models and migrations
Phase 3: Authentication and RBAC
Phase 4: Detection intake API
Phase 5: Enrichment engine
Phase 6: Risk scoring engine
Phase 7: Decision engine
Phase 8: Approval workflow
Phase 9: Response engine
Phase 10: Network device integration
Phase 11: Incident management
Phase 12: Audit logging
Phase 13: Dashboard
Phase 14: End-to-end integration
Phase 15: Security hardening
Phase 16: Comprehensive testing
Phase 17: Documentation completion
Phase 18: Production deployment

---

## 📝 Project Limitations

- **Lab-Only**: Designed for isolated laboratory environments; not suitable for production security operations
- **Single-Tenant**: No multi-tenancy support
- **Synchronous**: Initial implementation is synchronous; async background workers added in Phase 19
- **Mock Providers**: External enrichment providers are mocked for development
- **Limited Scalability**: Single-node PostgreSQL; no distributed cache initially

---

## 🔮 Future Improvements

- Asynchronous background workers (Celery/RQ)
- Redis caching for performance
- Real threat intelligence provider integration
- Real SIEM connectors (Splunk, ELK, QRadar)
- Real firewall connectors (Palo Alto, Fortinet)
- Machine learning-based risk scoring
- Multi-tenancy support
- Distributed audit logging
- High availability deployment
- Mobile dashboard app

---

## 🤝 Contributing

This is an academic graduation project. Contributions welcome from:
- Cybersecurity students
- Network engineers
- Backend developers
- Frontend developers
- DevOps engineers
- Security researchers

See [Development](docs/development.md) for setup instructions.

---

## ⚖️ License

This project is released as-is for educational purposes.

---

## 🛡️ Security Reporting

Do not open public issues for security vulnerabilities. Instead, email security concerns to the project maintainer.

See [SECURITY.md](SECURITY.md) for details.

---

## 📧 Contact

Developed by: **mahmoudaliOO7**  
Repository: [github.com/mahmoudaliOO7/ANSOP](https://github.com/mahmoudaliOO7/ANSOP)

---

**ANSOP: Building the next generation of security orchestration** 🔐

Last updated: 2025-08-18  
Phase: 1 (Foundation)
