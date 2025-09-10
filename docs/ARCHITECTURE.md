# Architecture Overview

This repository serves as a **configuration and infrastructure repository** for the robot scheduling research environment. The actual research code is managed in a separate repository and linked via git submodules.

## Repository Structure

### Configuration Repository (This Repo)
```
scheduling-config/
├── docker/                    # Docker configuration files
│   └── Dockerfile.research    # Research environment image
├── .devcontainer/            # Cursor/VS Code dev container config
├── scripts/                  # Setup and management scripts
│   ├── setup.sh             # Main setup script
│   └── add-research-repo.sh # Helper to add research repo
├── docs/                     # Documentation
│   ├── SETUP.md             # Setup guide
│   └── ARCHITECTURE.md      # This file
├── requirements/             # Python dependencies
│   ├── simple.txt           # Core dependencies
│   └── jupyter.txt          # Jupyter dependencies
├── research-code/            # Git submodule (research repository)
├── results/                  # Generated results (volume mounted)
├── test_cases/               # Test case files (volume mounted)
├── logs/                     # Log files (volume mounted)
├── docker-compose.yml        # Main Docker Compose configuration
├── Makefile                  # Common commands and shortcuts
└── README.md                 # Main documentation
```

### Research Repository (Submodule)
```
research-code/
├── src/
│   ├── algorithms/           # Scheduling algorithms
│   ├── common/              # Task/resource representations
│   ├── testing/             # Test framework
│   └── visualization/       # Visualization tools
├── tests/                   # Unit tests
├── notebooks/               # Jupyter notebooks
├── requirements/            # Python dependencies
└── research.py             # Main research script
```

## Key Benefits

### 1. **Separation of Concerns**
- **Configuration Repo**: Infrastructure, Docker, setup scripts
- **Research Repo**: Actual algorithms, tests, research code

### 2. **Reusability**
- Multiple researchers can use the same configuration
- Easy to switch between different research repositories
- Configuration can be shared across projects

### 3. **Version Control**
- Research code has its own version history
- Configuration changes are tracked separately
- Easy to update research code independently

### 4. **Development Flexibility**
- Researchers can work on their own repositories
- Configuration can be customized per project
- Easy to add new research repositories

## Docker Architecture

### Single Container Design
- **One container** with all necessary dependencies
- **Jupyter Lab** for interactive development
- **Volume mounting** for live code editing
- **No external dependencies** (Redis, PostgreSQL removed)

### Volume Mounts
```yaml
volumes:
  - ./research-code:/app/research-code    # Research code (submodule)
  - ./results:/app/results                # Generated results
  - ./test_cases:/app/test_cases          # Test case files
  - ./logs:/app/logs                      # Log files
```

### Environment Variables
```yaml
environment:
  - PYTHONPATH=/app:/app/research-code    # Python path includes research code
  - PYTHONUNBUFFERED=1                    # Unbuffered output
```

## Development Workflows

### 1. **Cursor/VS Code Development**
1. Open configuration repository in Cursor
2. Use "Remote-Containers: Reopen in Container"
3. Research code available in `/app/research-code/`
4. Make changes and test in container
5. Commit to research repository
6. Update submodule reference

### 2. **Jupyter Lab Development**
1. Start environment: `make up`
2. Access Jupyter: http://localhost:8888
3. Navigate to research-code directory
4. Develop in notebooks
5. Commit changes to research repository

### 3. **Command Line Development**
1. Start environment: `make up`
2. Connect to container: `docker exec -it scheduling-research /bin/bash`
3. Work in `/app/research-code/`
4. Test and commit changes

## Git Submodule Management

### Adding Research Repository
```bash
# Using helper script
./scripts/add-research-repo.sh <repo-url>

# Manual method
git submodule add <repo-url> research-code
```

### Updating Research Code
```bash
# Update to latest version
git submodule update --remote research-code

# Commit the update
git add research-code
git commit -m "Update research code submodule"
```

### Working with Changes
```bash
# Make changes in research-code/
cd research-code
git add .
git commit -m "Your changes"
git push

# Update submodule reference
cd ..
git add research-code
git commit -m "Update research code submodule"
```

## File Organization

### Configuration Files
- `docker-compose.yml`: Main Docker configuration
- `docker/Dockerfile.research`: Research environment image
- `.devcontainer/devcontainer.json`: Dev container configuration
- `Makefile`: Common commands and shortcuts

### Setup Scripts
- `scripts/setup.sh`: Main setup script
- `scripts/add-research-repo.sh`: Helper to add research repository

### Documentation
- `README.md`: Main documentation
- `docs/SETUP.md`: Detailed setup guide
- `docs/ARCHITECTURE.md`: This architecture overview

### Dependencies
- `requirements/simple.txt`: Core Python dependencies
- `requirements/jupyter.txt`: Jupyter-specific dependencies

## Benefits of This Architecture

1. **Modularity**: Clear separation between infrastructure and research code
2. **Reusability**: Configuration can be used with different research repositories
3. **Maintainability**: Each repository has a single responsibility
4. **Collaboration**: Multiple researchers can work on different repositories
5. **Flexibility**: Easy to add new research repositories or modify configuration
6. **Version Control**: Independent versioning of configuration and research code
7. **Development Experience**: Seamless development in containers with live editing

## Future Extensions

### Multiple Research Repositories
```bash
# Add multiple research repositories
git submodule add <repo1-url> research-code-1
git submodule add <repo2-url> research-code-2
```

### Environment Variations
```bash
# Different Docker configurations for different needs
docker-compose -f docker-compose.gpu.yml up    # GPU-enabled environment
docker-compose -f docker-compose.cluster.yml up # Cluster environment
```

### Automated Testing
```bash
# CI/CD integration
make test-all-repos    # Test all research repositories
make benchmark         # Run performance benchmarks
```
