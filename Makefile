# HRMS Project Makefile - International Standards Compliant
# Professional development automation for Python projects

.PHONY: help install clean test format lint security run dev setup quality all

# Default target
help:
	@echo "🏢 HRMS - Professional Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install all dependencies"
	@echo "  make setup       - Complete project setup"
	@echo ""
	@echo "🧹 Code Quality:"
	@echo "  make clean       - Clean cache and temporary files"
	@echo "  make format      - Format code with Black & isort"
	@echo "  make lint        - Run code quality checks"
	@echo "  make security    - Run security analysis"
	@echo "  make quality     - Run all quality checks"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test        - Run all tests"
	@echo "  make test-cov    - Run tests with coverage"
	@echo ""
	@echo "🚀 Development:"
	@echo "  make run         - Run HRMS application"
	@echo "  make dev         - Run in development mode"
	@echo ""
	@echo "🔄 Automation:"
	@echo "  make all         - Run complete CI/CD pipeline"

# Installation and setup
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install black isort autoflake pytest pytest-cov bandit safety
	@echo "✅ Dependencies installed successfully!"

setup: install
	@echo "🔧 Setting up project..."
	python -c "from src.models.models_enhanced import init_enhanced_database; init_enhanced_database()"
	@echo "✅ Project setup completed!"

# Code quality
clean:
	@echo "🧹 Cleaning project..."
	python cleanup.py
	@echo "✅ Project cleaned!"

format:
	@echo "🎨 Formatting code..."
	python format_code.py
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Running code quality checks..."
	python code_quality_check.py
	@echo "✅ Code quality check completed!"

security:
	@echo "🔒 Running security analysis..."
	python security_review.py
	@echo "✅ Security analysis completed!"

quality: clean format lint security
	@echo "✅ All quality checks completed!"

# Testing
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v
	@echo "✅ Tests completed!"

test-cov:
	@echo "🧪 Running tests with coverage..."
	python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "✅ Tests with coverage completed!"

# Development
run:
	@echo "🚀 Starting HRMS application..."
	python run.py

dev:
	@echo "🔧 Starting HRMS in development mode..."
	python run.py --dev

# Complete pipeline
all: clean format lint security test
	@echo "🎉 Complete CI/CD pipeline completed successfully!"
	@echo "📊 Project is ready for production!"

# Git operations
commit: quality
	@echo "📝 Committing changes..."
	git add .
	git commit -m "feat: automated code quality improvements"
	@echo "✅ Changes committed!"

push: commit
	@echo "🚀 Pushing to repository..."
	git push
	@echo "✅ Changes pushed!"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation generation not implemented yet"

# Docker operations (future)
docker-build:
	@echo "🐳 Building Docker image..."
	@echo "Docker build not implemented yet"

docker-run:
	@echo "🐳 Running Docker container..."
	@echo "Docker run not implemented yet"

# Performance testing
perf:
	@echo "⚡ Running performance tests..."
	@echo "Performance testing not implemented yet"

# Deployment
deploy:
	@echo "🚀 Deploying application..."
	@echo "Deployment not implemented yet"
