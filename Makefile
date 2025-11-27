.PHONY: help install install-dev clean test coverage lint format type-check quality run docker-build docker-up docker-down docker-logs setup

.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy

# Directories
SRC_DIR := app
TEST_DIR := tests
DOCKER_DIR := docker

# Colors for output
COLOR_RESET := \033[0m
COLOR_BOLD := \033[1m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m

help: ## Show this help message
	@echo "$(COLOR_BOLD)Resume Parser Framework - Available Commands$(COLOR_RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""

# Installation targets
install: ## Install production dependencies
	@echo "$(COLOR_BLUE)Installing production dependencies...$(COLOR_RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(COLOR_GREEN)✓ Production dependencies installed$(COLOR_RESET)"

install-dev: ## Install development dependencies
	@echo "$(COLOR_BLUE)Installing development dependencies...$(COLOR_RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	@echo "$(COLOR_GREEN)✓ Development dependencies installed$(COLOR_RESET)"

setup: install-dev ## Complete development environment setup
	@echo "$(COLOR_BLUE)Setting up development environment...$(COLOR_RESET)"
	@mkdir -p logs tmp uploads
	@cp -n .env.example .env 2>/dev/null || true
	@echo "$(COLOR_GREEN)✓ Development environment ready$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Note: Update .env file with your configuration$(COLOR_RESET)"

# Cleaning targets
clean: ## Clean up generated files and caches
	@echo "$(COLOR_BLUE)Cleaning up...$(COLOR_RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage coverage.xml
	@echo "$(COLOR_GREEN)✓ Cleanup complete$(COLOR_RESET)"

# Testing targets
test: ## Run all tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	$(PYTEST) $(TEST_DIR) -v

test-unit: ## Run unit tests only
	@echo "$(COLOR_BLUE)Running unit tests...$(COLOR_RESET)"
	$(PYTEST) $(TEST_DIR)/unit -v

test-integration: ## Run integration tests only
	@echo "$(COLOR_BLUE)Running integration tests...$(COLOR_RESET)"
	$(PYTEST) $(TEST_DIR)/integration -v

test-fast: ## Run tests without slow tests
	@echo "$(COLOR_BLUE)Running fast tests...$(COLOR_RESET)"
	$(PYTEST) $(TEST_DIR) -v -m "not slow"

coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=html --cov-report=term --cov-report=xml
	@echo "$(COLOR_GREEN)✓ Coverage report generated in htmlcov/index.html$(COLOR_RESET)"

coverage-report: ## Open coverage report in browser
	@echo "$(COLOR_BLUE)Opening coverage report...$(COLOR_RESET)"
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "$(COLOR_YELLOW)Please open htmlcov/index.html manually$(COLOR_RESET)"

# Code quality targets
format: ## Format code with Black and isort
	@echo "$(COLOR_BLUE)Formatting code...$(COLOR_RESET)"
	$(BLACK) $(SRC_DIR) $(TEST_DIR)
	$(ISORT) $(SRC_DIR) $(TEST_DIR)
	@echo "$(COLOR_GREEN)✓ Code formatted$(COLOR_RESET)"

lint: ## Run linting with Ruff
	@echo "$(COLOR_BLUE)Running linter...$(COLOR_RESET)"
	$(RUFF) check $(SRC_DIR) $(TEST_DIR)

lint-fix: ## Run linting and fix auto-fixable issues
	@echo "$(COLOR_BLUE)Running linter with auto-fix...$(COLOR_RESET)"
	$(RUFF) check --fix $(SRC_DIR) $(TEST_DIR)

type-check: ## Run type checking with MyPy
	@echo "$(COLOR_BLUE)Running type checker...$(COLOR_RESET)"
	$(MYPY) $(SRC_DIR)

quality: format lint type-check ## Run all code quality checks
	@echo "$(COLOR_GREEN)✓ All quality checks passed$(COLOR_RESET)"

# CI/CD simulation
ci: clean install-dev quality coverage ## Run CI pipeline locally
	@echo "$(COLOR_GREEN)✓ CI pipeline completed successfully$(COLOR_RESET)"

# Docker targets
docker-build: ## Build Docker image
	@echo "$(COLOR_BLUE)Building Docker image...$(COLOR_RESET)"
	docker build -f $(DOCKER_DIR)/Dockerfile -t resume-parser:latest .
	@echo "$(COLOR_GREEN)✓ Docker image built$(COLOR_RESET)"

docker-build-dev: ## Build Docker image for development
	@echo "$(COLOR_BLUE)Building development Docker image...$(COLOR_RESET)"
	docker build -f $(DOCKER_DIR)/Dockerfile.dev -t resume-parser:dev .
	@echo "$(COLOR_GREEN)✓ Development Docker image built$(COLOR_RESET)"

docker-up: ## Start Docker containers
	@echo "$(COLOR_BLUE)Starting Docker containers...$(COLOR_RESET)"
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml up -d
	@echo "$(COLOR_GREEN)✓ Docker containers started$(COLOR_RESET)"

docker-down: ## Stop Docker containers
	@echo "$(COLOR_BLUE)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml down
	@echo "$(COLOR_GREEN)✓ Docker containers stopped$(COLOR_RESET)"

docker-logs: ## Show Docker container logs
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml logs -f

docker-shell: ## Open shell in Docker container
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml exec app /bin/bash

docker-test: ## Run tests in Docker container
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml exec app pytest

docker-clean: ## Remove Docker containers and images
	@echo "$(COLOR_BLUE)Cleaning Docker resources...$(COLOR_RESET)"
	docker-compose -f $(DOCKER_DIR)/docker-compose.yml down -v --rmi all
	@echo "$(COLOR_GREEN)✓ Docker cleanup complete$(COLOR_RESET)"

# Development targets
run: ## Run the application locally
	@echo "$(COLOR_BLUE)Starting application...$(COLOR_RESET)"
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run the application in production mode
	@echo "$(COLOR_BLUE)Starting application (production mode)...$(COLOR_RESET)"
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000

shell: ## Open Python REPL with app context
	@echo "$(COLOR_BLUE)Starting Python shell...$(COLOR_RESET)"
	$(PYTHON) -i -c "from app.config import settings; from app.core.models import ResumeData; print('Available: settings, ResumeData')"

# Security targets
security-check: ## Check for security vulnerabilities
	@echo "$(COLOR_BLUE)Checking for security vulnerabilities...$(COLOR_RESET)"
	$(PIP) install --upgrade pip-audit
	$(PYTHON) -m pip_audit

# Documentation targets
docs: ## Generate documentation
	@echo "$(COLOR_BLUE)Generating documentation...$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Documentation generation not yet implemented$(COLOR_RESET)"

# Utility targets
requirements: ## Generate requirements.txt from installed packages
	@echo "$(COLOR_BLUE)Generating requirements.txt...$(COLOR_RESET)"
	$(PIP) freeze > requirements-freeze.txt
	@echo "$(COLOR_GREEN)✓ Requirements saved to requirements-freeze.txt$(COLOR_RESET)"

upgrade-deps: ## Upgrade all dependencies
	@echo "$(COLOR_BLUE)Upgrading dependencies...$(COLOR_RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements-dev.txt
	@echo "$(COLOR_GREEN)✓ Dependencies upgraded$(COLOR_RESET)"

show-config: ## Show current configuration
	@echo "$(COLOR_BOLD)Current Configuration:$(COLOR_RESET)"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pip: $$($(PIP) --version)"
	@echo "Source directory: $(SRC_DIR)"
	@echo "Test directory: $(TEST_DIR)"

.PHONY: all
all: clean install-dev quality coverage ## Run full development workflow
	@echo "$(COLOR_GREEN)✓ Full development workflow completed$(COLOR_RESET)"
