# Spacecraft Scheduler Configuration

This repository contains the Docker configuration and infrastructure setup for the spacecraft scheduler development environment. The actual scheduler code is managed in a separate repository and linked via git submodules.

## 🏗️ Repository Structure

```
spacecraft_scheduler_config/
├── docker/                    # Docker configuration files
├── .devcontainer/            # Cursor/VS Code development container config
├── scripts/                  # Setup and management scripts
├── docs/                     # Documentation
├── spacecraft_scheduler/     # Git submodule (main scheduler repository)
├── data/                     # Persistent data directory
├── results/                  # Persistent results directory
├── logs/                     # Persistent logs directory
└── docker-compose.yml        # Main Docker Compose configuration
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup
1. **Clone this repository:**
   ```bash
   git clone <this-repo-url>
   cd spacecraft_scheduler_config
   ```

2. **Add the spacecraft scheduler submodule:**
   ```bash
   ./scripts/add-spacecraft-scheduler.sh <spacecraft-scheduler-repo-url>
   ```

3. **Build and start the development environment:**
   ```bash
   make build
   make up
   ```

4. **Access the environment:**
   - **Jupyter Lab**: http://localhost:8888
   - **Cursor Dev Container**: Use "Remote-Containers: Reopen in Container"

## 📋 Available Commands

```bash
make help          # Show all available commands
make build         # Build Docker image with spacecraft scheduler dependencies
make up            # Start development environment
make down          # Stop development environment
make jupyter       # Show Jupyter Lab access info
make clean         # Clean up containers and volumes
```

## 🔧 Development Workflow

### Using Cursor/VS Code
1. Open this repository in Cursor
2. Use "Remote-Containers: Reopen in Container"
3. The spacecraft scheduler code will be available in `/app/spacecraft_scheduler/`
4. All your changes will be reflected in the container

### Using Jupyter Lab
1. Run `make up`
2. Open http://localhost:8888 in your browser
3. Navigate to the spacecraft_scheduler directory
4. Open and run the development notebooks

### Command Line Development
1. Run `make up`
2. Connect to the container: `docker exec -it spacecraft-scheduler-dev /bin/bash`
3. Navigate to `/app/spacecraft_scheduler/` to access the scheduler code

## 📁 Submodule Management

### Adding the Spacecraft Scheduler Repository
```bash
# Add your spacecraft scheduler repository as a submodule
git submodule add <spacecraft-scheduler-repo-url> spacecraft_scheduler

# Initialize and update submodules
git submodule update --init --recursive
```

### Updating Spacecraft Scheduler Code
```bash
# Update to latest version of spacecraft scheduler code
git submodule update --remote spacecraft_scheduler

# Commit the submodule update
git add spacecraft_scheduler
git commit -m "Update spacecraft scheduler submodule"
```

### Working with Submodules
```bash
# Clone this repo with submodules
git clone --recursive <this-repo-url>

# Or if already cloned, initialize submodules
git submodule update --init --recursive
```

## 🐳 Docker Configuration

The Docker setup includes:
- **Single Container**: Python 3.10 with all spacecraft scheduler dependencies
- **Build Time Dependencies**: Submodule requirements installed during build
- **Jupyter Lab**: Interactive development environment
- **Volume Mounting**: Live code editing from host
- **Persistent Storage**: Data, results, and logs persist across restarts

## 📊 Development Environment Features

- **Algorithm Development**: Test and develop spacecraft scheduling algorithms
- **Test Case Management**: Create and manage test scenarios
- **Performance Visualization**: Generate charts and reports
- **Interactive Development**: Jupyter notebooks for experimentation
- **Persistent Data**: All data, results, and logs persist across container restarts

## 🔄 Workflow for Algorithm Development

1. **Develop algorithms** in the spacecraft_scheduler repository
2. **Test locally** using the Docker environment
3. **Compare performance** using the built-in framework
4. **Visualize results** with generated charts and reports
5. **Commit changes** to the spacecraft_scheduler repository
6. **Update submodule** in this configuration repository

## 📝 Configuration Files

- `docker-compose.yml`: Main Docker Compose configuration
- `docker/Dockerfile`: Spacecraft scheduler development Docker image
- `.devcontainer/devcontainer.json`: Cursor/VS Code development container
- `scripts/add-spacecraft-scheduler.sh`: Script to add spacecraft scheduler submodule
- `Makefile`: Common commands and shortcuts

## 🤝 Contributing

1. Make changes to the spacecraft scheduler code in the spacecraft_scheduler submodule
2. Test your changes using this configuration environment
3. Commit changes to the spacecraft_scheduler repository
4. Update the submodule reference in this repository
5. Submit a pull request with both repository updates

## 📞 Support

For issues with:
- **Docker/Infrastructure**: Create an issue in this repository
- **Spacecraft Scheduler Code/Algorithms**: Create an issue in the spacecraft_scheduler repository

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Get up and running in 5 minutes
- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Architecture Overview](docs/ARCHITECTURE.md) - System architecture and design decisions
- [Requirements Management](docs/REQUIREMENTS.md) - Managing Python dependencies