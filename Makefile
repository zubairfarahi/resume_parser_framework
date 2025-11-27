# Resume Parser Framework - Makefile
# Simple commands for development

.PHONY: help install install-dev test lint format clean run docker-build docker-run

# Default target
help:
	@echo "Resume Parser Framework - Available Commands"
	@echo "============================================="
	@echo "make install       - Install production dependencies"
	@echo "make install-dev   - Install all dependencies (dev + prod)"
	@echo "make test          - Run all tests"
	@echo "make test-unit     - Run unit tests only"
	@echo "make test-cov      - Run tests with coverage report"
	@echo "make lint          - Run all linters (black, isort, ruff, mypy)"
	@echo "make format        - Format code with black and isort"
	@echo "make run           - Start the FastAPI server"
	@echo "make clean         - Clean up temporary files"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-run    - Run Docker container"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install all dependencies (development + production)
install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run all tests
test:
	pytest tests/ -v

# Run unit tests only
test-unit:
	pytest tests/unit -v

# Run integration tests only
test-integration:
	pytest tests/integration -v

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=term --cov-report=html --cov-report=xml

# Run tests with coverage and fail if below threshold
test-cov-check:
	pytest --cov=app --cov-report=term --cov-fail-under=80

# Run all linters
lint:
	@echo "Running Black..."
	black --check app tests examples
	@echo "Running isort..."
	isort --check-only app tests examples
	@echo "Running Ruff..."
	ruff check app tests examples
	@echo "Running MyPy..."
	mypy app --ignore-missing-imports

# Format code
format:
	@echo "Formatting with Black..."
	black app tests examples
	@echo "Sorting imports with isort..."
	isort app tests examples

# Start the FastAPI server
run:
	python main.py

# Start with uvicorn directly
run-uvicorn:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ coverage.xml .coverage 2>/dev/null || true

# Build Docker image
docker-build:
	docker build -t resume-parser:latest .

# Run Docker container
docker-run:
	docker run -d -p 8000:8000 --name resume-parser \
		-e OPENAI_API_KEY=$${OPENAI_API_KEY} \
		resume-parser:latest

# Stop Docker container
docker-stop:
	docker stop resume-parser || true
	docker rm resume-parser || true

# View Docker logs
docker-logs:
	docker logs -f resume-parser
