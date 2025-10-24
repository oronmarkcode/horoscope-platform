.PHONY: help install-backend install-frontend start-backend start-frontend start-all test clean db-up db-down db-reset migrate init-db

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-backend: ## Install backend dependencies
	cd backend && poetry install

install-frontend: ## Install frontend dependencies
	cd frontend && npm install

install: install-backend install-frontend ## Install all dependencies

start-backend: ## Start the backend development server
	cd backend && poetry run uvicorn horoscope_backend.main:app --reload --host 0.0.0.0 --port 8000

start-frontend: ## Start the frontend development server
	cd frontend && npm run dev

start-all: ## Start all services with docker-compose
	docker-compose up -d

test: ## Run backend tests
	cd backend && poetry run pytest

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +

db-up: ## Start PostgreSQL database
	docker-compose up -d postgres

db-down: ## Stop PostgreSQL database
	docker-compose down

db-reset: ## Reset database (stop, remove volumes, start)
	docker-compose down -v
	docker-compose up -d postgres

migrate: ## Run database migrations
	cd backend && poetry run alembic upgrade head

init-db: ## Initialize database with sample data
	cd backend && poetry run python init_db.py

setup: ## Complete setup (install, db-up, migrate, init-db)
	$(MAKE) install-backend
	$(MAKE) db-up
	sleep 5
	$(MAKE) migrate
	$(MAKE) init-db

dev: ## Start development environment (backend + database)
	$(MAKE) db-up
	sleep 3
	$(MAKE) start-backend
