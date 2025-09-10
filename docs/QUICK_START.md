# Quick Start Guide

This guide will get you up and running with the spacecraft scheduler development environment in minutes.

## 🚀 **5-Minute Setup**

### 1. Clone Configuration Repository
```bash
git clone <this-config-repo-url>
cd spacecraft_scheduler_config
```

### 2. Add Spacecraft Scheduler Submodule
```bash
./scripts/add-spacecraft-scheduler.sh <spacecraft-scheduler-repo-url>
```

### 3. Build and Start Environment
```bash
make build
make up
```

### 4. Access Development Environment
- **Jupyter Lab**: http://localhost:8888
- **Cursor Dev Container**: Use "Remote-Containers: Reopen in Container"

## 📁 **Repository Structure**

```
spacecraft_scheduler_config/
├── docker/                    # Docker configuration
├── .devcontainer/            # Cursor dev container config
├── scripts/                  # Setup scripts
├── docs/                     # Documentation
├── spacecraft_scheduler/     # Git submodule (your scheduler code)
├── data/                     # Persistent data directory
├── results/                  # Persistent results directory
├── logs/                     # Persistent logs directory
└── docker-compose.yml        # Docker Compose configuration
```

## 🔧 **Available Commands**

```bash
make help          # Show all commands
make build         # Build Docker image with dependencies
make up            # Start development environment
make down          # Stop development environment
make jupyter       # Show Jupyter Lab access info
make clean         # Clean up containers and volumes
```

## 🎯 **Development Workflow**

### Using Cursor/VS Code
1. Open this repository in Cursor
2. Use "Remote-Containers: Reopen in Container"
3. Your spacecraft scheduler code is in `/app/spacecraft_scheduler/`
4. Make changes and test in the container
5. Commit to spacecraft scheduler repository
6. Update submodule reference

### Using Jupyter Lab
1. Start environment: `make up`
2. Open http://localhost:8888
3. Navigate to `spacecraft_scheduler/` directory
4. Develop in notebooks
5. Commit changes to spacecraft scheduler repository

## 📊 **Persistent Data**

The following directories persist across container restarts:
- `data/` - Input data files
- `results/` - Generated results and outputs
- `logs/` - Application logs

These directories are owned by the configuration repository and shared with the spacecraft scheduler submodule.

## 🔄 **Updating Code**

### Update Spacecraft Scheduler
```bash
git submodule update --remote spacecraft_scheduler
git add spacecraft_scheduler
git commit -m "Update spacecraft scheduler submodule"
```

### Make Changes to Spacecraft Scheduler
```bash
cd spacecraft_scheduler
# Make your changes
git add .
git commit -m "Your changes"
git push
cd ..
git add spacecraft_scheduler
git commit -m "Update spacecraft scheduler submodule"
```

## 🐳 **Docker Details**

- **Single Container**: All dependencies installed at build time
- **Build Time Dependencies**: Submodule requirements installed during build
- **Volume Mounting**: Live code editing from host
- **Persistent Storage**: Data, results, and logs persist across restarts

## 🆘 **Troubleshooting**

### Container Won't Start
```bash
# Check logs
docker-compose logs spacecraft_scheduler

# Rebuild
make clean
make build
make up
```

### Submodule Issues
```bash
# Reinitialize submodule
git submodule deinit spacecraft_scheduler
git submodule update --init spacecraft_scheduler
```

### Missing Dependencies
```bash
# Rebuild container
make build
```

## 📚 **Next Steps**

1. **Develop algorithms** in the spacecraft_scheduler repository
2. **Test using Docker** environment
3. **Compare performance** using built-in framework
4. **Visualize results** with generated charts
5. **Commit changes** to spacecraft scheduler repository
6. **Update submodule** in this configuration repository

## 🔗 **Related Documentation**

- [Setup Guide](SETUP.md) - Detailed setup instructions
- [Architecture Overview](ARCHITECTURE.md) - System architecture
- [Requirements Management](REQUIREMENTS.md) - Dependency management
