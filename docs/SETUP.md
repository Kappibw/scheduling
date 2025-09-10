# Setup Guide

This guide will help you set up the spacecraft scheduler development environment with git submodules.

## Prerequisites

- Docker and Docker Compose
- Git
- Your research repository (the one with the actual code)

## Quick Setup

### 1. Clone This Configuration Repository

```bash
git clone <this-config-repo-url>
cd spacecraft_scheduler_config
```

### 2. Add the Spacecraft Scheduler Repository as a Submodule

```bash
# Use the helper script
./scripts/add-spacecraft-scheduler.sh <spacecraft-scheduler-repo-url>

# Or manual setup
git submodule add <spacecraft-scheduler-repo-url> spacecraft_scheduler
```

### 3. Build the Development Environment

```bash
# Build the container with all dependencies
make build
```

### 4. Start the Development Environment

```bash
make up
```

### 5. Access the Environment

- **Jupyter Lab**: http://localhost:8888
- **Cursor Dev Container**: Use "Remote-Containers: Reopen in Container"

## Detailed Setup

### Step 1: Prepare Your Spacecraft Scheduler Repository

Your spacecraft scheduler repository should have this structure:
```
spacecraft_scheduler/
├── src/
│   ├── algorithms/        # Your scheduling algorithms
│   ├── common/           # Task/resource representations
│   ├── testing/          # Test framework
│   └── visualization/    # Visualization tools
├── tests/                # Unit tests
├── notebooks/            # Jupyter notebooks
├── requirements/         # Python dependencies
└── main.py              # Main scheduler script
```

### Step 2: Add as Submodule

```bash
# Using the helper script (recommended)
./scripts/add-spacecraft-scheduler.sh https://github.com/yourusername/spacecraft_scheduler.git

# Or manually
git submodule add https://github.com/yourusername/spacecraft_scheduler.git spacecraft_scheduler
```

### Step 3: Initialize Submodules

```bash
git submodule update --init --recursive
```

### Step 4: Build and Start

```bash
make build
make up
```

## Working with Submodules

### Updating Spacecraft Scheduler Code

```bash
# Update to latest version
git submodule update --remote spacecraft_scheduler

# Commit the update
git add spacecraft_scheduler
git commit -m "Update spacecraft scheduler submodule"
```

### Making Changes to Spacecraft Scheduler Code

1. **Edit code** in the `spacecraft_scheduler/` directory
2. **Test changes** using the Docker environment
3. **Commit to spacecraft scheduler repository**:
   ```bash
   cd spacecraft_scheduler
   git add .
   git commit -m "Your changes"
   git push
   ```
4. **Update submodule reference**:
   ```bash
   cd ..
   git add spacecraft_scheduler
   git commit -m "Update spacecraft scheduler submodule"
   ```

### Cloning with Submodules

```bash
# Clone with submodules
git clone --recursive <this-config-repo-url>

# Or if already cloned
git submodule update --init --recursive
```

## Development Workflow

### Using Cursor/VS Code

1. Open this configuration repository in Cursor
2. Use "Remote-Containers: Reopen in Container"
3. The research code will be available in `/app/research-code/`
4. Make changes to the research code
5. Test using the Docker environment
6. Commit changes to the research repository
7. Update submodule reference

### Using Jupyter Lab

1. Run `make up`
2. Open http://localhost:8888
3. Navigate to `research-code/` directory
4. Open and run notebooks
5. Make changes and test
6. Commit to research repository

### Command Line Development

1. Run `make up`
2. Connect to container: `docker exec -it scheduling-research /bin/bash`
3. Navigate to `/app/research-code/`
4. Make changes and test
5. Commit to research repository

## Troubleshooting

### Submodule Issues

```bash
# If submodule is in detached HEAD state
cd research-code
git checkout main  # or your default branch
git pull

# If submodule update fails
git submodule deinit research-code
git submodule update --init research-code
```

### Docker Issues

```bash
# Rebuild everything
make clean
make build
make up

# Check container logs
docker-compose logs research
```

### Permission Issues

```bash
# Fix script permissions
chmod +x scripts/*.sh
```

## File Structure After Setup

```
scheduling-config/
├── docker/                    # Docker configuration
├── .devcontainer/            # Dev container config
├── scripts/                  # Setup scripts
├── docs/                     # Documentation
├── requirements/             # Python dependencies
├── research-code/            # Git submodule (your research repo)
├── results/                  # Generated results
├── test_cases/               # Test case files
├── logs/                     # Log files
├── docker-compose.yml        # Docker Compose config
├── Makefile                  # Common commands
└── README.md                 # This file
```

## Next Steps

1. **Develop algorithms** in the research-code repository
2. **Test using Docker** environment
3. **Compare performance** using built-in framework
4. **Visualize results** with generated charts
5. **Commit changes** to research repository
6. **Update submodule** in this configuration repository
