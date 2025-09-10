# Makefile for Robot Scheduling Research System

.PHONY: help build up down clean test lint format install dev research

# Default target
help:
	@echo "Robot Scheduling Research System - Available commands:"
	@echo "  build     - Build research Docker image"
	@echo "  up        - Start research environment"
	@echo "  down      - Stop research environment"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  install   - Install dependencies locally"
	@echo "  dev       - Start development environment"
	@echo "  research  - Run algorithm research and comparison"
	@echo "  jupyter   - Start Jupyter Lab"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Development commands
install:
	pip install -r requirements/simple.txt

dev:
	pip install -r requirements/simple.txt -r requirements/jupyter.txt

# Testing and quality
test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Data and results directories
setup-dirs:
	mkdir -p results test_cases logs

# Setup submodules
setup:
	./scripts/setup.sh

# Research commands
research:
	docker-compose exec research bash -c "cd /app/research-code && python research.py"

jupyter:
	@echo "Jupyter Lab available at: http://localhost:8888"
	@echo "No password required for development"
	@echo "Research code is available in /app/research-code/"

# Run demo
demo:
	python src/main.py --demo

# Run with custom data
run:
	python src/main.py --tasks data/tasks.json --resources data/resources.json

# Full setup
setup: setup-dirs install
	@echo "Setup complete! Run 'make research' to test the system."
