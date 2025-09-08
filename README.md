# Robot Scheduling System

A modular, dockerized system for scheduling robot tasks with resource tracking and multiple algorithm support.

## Project Structure

```
scheduling/
├── src/
│   ├── common/           # Shared libraries
│   │   ├── tasks/        # Task definitions and management
│   │   ├── resources/    # Resource tracking and management
│   │   └── visualization/ # Schedule visualization tools
│   ├── algorithms/       # Scheduling algorithms
│   │   ├── milp/         # MILP solver implementation
│   │   └── base/         # Base algorithm interface
│   └── main.py          # Main application entry point
├── tests/               # Test suite
├── docker/              # Docker configuration
├── requirements/        # Python dependencies
└── docs/               # Documentation
```

## Features

- **Modular Design**: Easy to swap scheduling algorithms
- **Resource Tracking**: Monitor and manage robot resources
- **Visualization**: Visual representation of schedules
- **Dockerized**: Containerized deployment
- **MILP Solver**: Mixed Integer Linear Programming for optimal scheduling

## Quick Start

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run locally
pip install -r requirements/base.txt
python src/main.py
```

## Development

```bash
# Install development dependencies
pip install -r requirements/dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/
```
