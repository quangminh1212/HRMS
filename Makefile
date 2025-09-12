.PHONY: help install install-dev run test lint format clean init-db sample-data docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  run          Run the development server"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean up generated files"
	@echo "  init-db      Initialize database"
	@echo "  sample-data  Load sample data"

# Install dependencies
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Run application
run:
	python run.py

# Testing
test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=. --cov-report=html

# Code quality
lint:
	flake8 .
	mypy .

format:
	black .
	isort .

# Database operations
init-db:
	python -c "from run import initialize_database; initialize_database()"

sample-data:
	python init_sample_data.py

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf build/ dist/ *.egg-info/

# Docker operations (if needed)
docker-build:
	docker build -t hrms .

docker-run:
	docker run -p 5000:5000 hrms
