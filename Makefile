# Makefile for Spacecraft Scheduler Configuration

.PHONY: help build up down clean setup-dirs jupyter setup

# Default target
help:
	@echo "Spacecraft Scheduler Configuration - Available commands:"
	@echo "  build     - Build Docker image with spacecraft scheduler dependencies"
	@echo "  up        - Start development environment"
	@echo "  down      - Stop development environment"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  jupyter   - Show Jupyter Lab access info"

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

# Data and results directories
setup-dirs:
	mkdir -p data results logs

# Development commands
jupyter:
	@echo "Jupyter Lab available at: http://localhost:8888"
	@echo "No password required for development"
	@echo "Spacecraft scheduler code is available in /app/spacecraft_scheduler/"

# Full setup
setup: setup-dirs
	@echo "Setup complete! Next steps:"
	@echo "  1. Add spacecraft scheduler submodule: ./scripts/add-spacecraft-scheduler.sh <repo-url>"
	@echo "  2. Build container: make build"
	@echo "  3. Start environment: make up"