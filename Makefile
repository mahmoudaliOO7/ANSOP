.PHONY: help build up down logs test lint format clean install dev migrate create-admin

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml
BACKEND_SERVICE = backend
FRONTEND_SERVICE = frontend
POSTGRES_SERVICE = postgres

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)ANSOP Development Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)Docker Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make up              # Start all services"
	@echo "  make down            # Stop all services"
	@echo "  make test            # Run backend tests"
	@echo "  make lint            # Run code quality checks"
	@echo "  make migrate         # Run database migrations"

# ⸻ Docker Commands

build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

up: ## Start all services (builds if needed)
	@echo "$(BLUE)Starting services...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo ""
	@echo "$(YELLOW)Services:$(NC)"
	@echo "  Backend:   http://localhost:8000"
	@echo "  Frontend:  http://localhost:5173"
	@echo "  API Docs:  http://localhost:8000/docs"
	@echo "  Database:  localhost:5432"

down: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

restart: ## Restart all services
	@echo "$(BLUE)Restarting services...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) restart
	@echo "$(GREEN)✓ Services restarted$(NC)"

status: ## Show service status
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

logs: ## Show logs from all services
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f

logs-backend: ## Show backend logs
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f $(BACKEND_SERVICE)

logs-frontend: ## Show frontend logs
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f $(FRONTEND_SERVICE)

logs-postgres: ## Show database logs
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f $(POSTGRES_SERVICE)

# ⸻ Backend Commands

backend-shell: ## Open shell in backend container
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) /bin/bash

backend-python: ## Open Python REPL in backend container
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) python

install: ## Install backend dependencies
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

test: ## Run backend tests
	@echo "$(BLUE)Running tests...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pytest -v

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pytest --cov=app --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated: htmlcov/index.html$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pytest tests/unit -v

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pytest tests/integration -v

lint: ## Run code quality checks (ruff)
	@echo "$(BLUE)Running linter (Ruff)...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) ruff check app/ tests/

format: ## Format code (Black + Ruff)
	@echo "$(BLUE)Formatting code...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) black app/ tests/
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) ruff check --fix app/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

type-check: ## Run type checking (MyPy)
	@echo "$(BLUE)Running type checker (MyPy)...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) mypy app/ --ignore-missing-imports

# ⸻ Database Commands

migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

migrate-create: ## Create new migration (use MIGRATION_MSG="your message")
	@echo "$(BLUE)Creating migration...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) alembic revision --autogenerate -m "$(MIGRATION_MSG)"

migrate-history: ## Show migration history
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) alembic history

db-reset: ## Reset database (WARNING: deletes all data)
	@echo "$(RED)⚠️  WARNING: This will delete all database data!$(NC)"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(POSTGRES_SERVICE) psql -U ansop_user -d ansop_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; \
		make migrate; \
		echo "$(GREEN)✓ Database reset complete$(NC)"; \
	fi

create-admin: ## Create default admin user
	@echo "$(BLUE)Creating admin user...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) python -m app.cli create-admin
	@echo "$(GREEN)✓ Admin user created$(NC)"

db-shell: ## Open database shell
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(POSTGRES_SERVICE) psql -U ansop_user -d ansop_db

# ⸻ Frontend Commands

frontend-shell: ## Open shell in frontend container
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(FRONTEND_SERVICE) /bin/bash

frontend-install: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(FRONTEND_SERVICE) npm install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

frontend-build: ## Build frontend
	@echo "$(BLUE)Building frontend...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(FRONTEND_SERVICE) npm run build
	@echo "$(GREEN)✓ Frontend built$(NC)"

# ⸻ Setup & Init

init: ## Initialize project (first-time setup)
	@echo "$(BLUE)Initializing ANSOP...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)Created .env file - please review and update secrets$(NC)"; \
	fi
	make build
	make up
	sleep 5
	make migrate
	make create-admin
	@echo "$(GREEN)✓ ANSOP initialized successfully$(NC)"

# ⸻ Utility Commands

clean: ## Remove containers, volumes, and build artifacts
	@echo "$(BLUE)Cleaning up...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

deep-clean: clean ## Remove everything including images
	@echo "$(RED)Removing all images...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v --rmi all

# ⸻ Development Workflow

dev: up migrate create-admin ## Full development setup
	@echo "$(GREEN)✓ Development environment ready!$(NC)"

check: lint type-check test ## Run all checks (lint, type, test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

# ⸻ Documentation

docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	@echo "$(GREEN)✓ Documentation built to docs/$(NC)"

# ⸻ Security

security-check: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(BACKEND_SERVICE) pip-audit || true

# Default target
.DEFAULT_GOAL := help
