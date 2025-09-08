# Makefile for Robot Scheduling System

.PHONY: help build up down clean test lint format install dev

# Default target
help:
	@echo "Robot Scheduling System - Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  install   - Install dependencies locally"
	@echo "  dev       - Start development environment"

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
	pip install -r requirements/base.txt

dev:
	pip install -r requirements/dev.txt
	pre-commit install

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
	mkdir -p data results logs notebooks

# Run demo
demo:
	python src/main.py --demo

# Run with custom data
run:
	python src/main.py --tasks data/tasks.json --resources data/resources.json

# Jupyter notebook
notebook:
	docker-compose up jupyter

# Full setup
setup: setup-dirs install
	@echo "Setup complete! Run 'make demo' to test the system."
