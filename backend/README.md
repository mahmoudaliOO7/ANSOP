# Backend Application

FastAPI-based backend service for ANSOP security orchestration platform.

## Structure

```
backend/
├── app/
│   ├── api/              # REST API endpoints
│   ├── core/             # Configuration and core utilities
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic services
│   ├── engines/          # Security engines (detection, enrichment, etc.)
│   ├── connectors/       # External system integrations
│   ├── middleware/       # Request/response middleware
│   ├── main.py           # Application entry point
│   └── cli.py            # CLI commands
├── alembic/              # Database migrations
├── tests/                # Test suite
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
└── pytest.ini            # Pytest configuration
```

## Getting Started

### Local Development

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Docker Development

```bash
# Build and run with Docker Compose
cd ..
make up

# Run migrations
make migrate

# Create admin user
make create-admin
```

## Database

ANSOP uses PostgreSQL with Alembic for schema versioning.

### Creating Migrations

```bash
# Create a new migration (auto-detect changes)
make migrate-create MIGRATION_MSG="Add new table"

# Or manually
alembic revision --autogenerate -m "Add new table"

# Apply migrations
make migrate

# View migration history
make migrate-history
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test suite
make test-unit
make test-integration
```

## Code Quality

```bash
# Lint with Ruff
make lint

# Format code
make format

# Type checking with MyPy
make type-check
```

## API Documentation

When running, API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Environment Configuration

See `.env.example` in project root for all available settings.

Key variables:
- `DATABASE_URL` — PostgreSQL connection string
- `JWT_SECRET_KEY` — Secret key for JWT tokens
- `LAB_MODE` — Restrict responses to lab devices
- `DRY_RUN` — Simulate responses without executing

## Security Considerations

- All API endpoints require authentication (JWT tokens)
- Sensitive operations require RBAC validation
- All inputs validated with Pydantic schemas
- Database queries use SQLAlchemy ORM (SQL injection prevention)
- Passwords hashed with bcrypt
- No sensitive data logged (passwords, tokens, keys)

## Performance

- Database connection pooling enabled
- Indexes on commonly queried fields
- Async support ready for background tasks
- CORS configured for frontend integration

## Debugging

Enable debug logging:

```bash
export APP_LOG_LEVEL=DEBUG
make logs-backend
```

## Common Tasks

```bash
# Open Python REPL in backend container
make backend-python

# Open shell in backend container
make backend-shell

# View database
make db-shell

# Reset database (deletes all data)
make db-reset
```

---

**Phase**: 2 (Database Models & Migrations)  
**Status**: In Development
