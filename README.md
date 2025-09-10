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
make setup         # Initialize submodules and setup environment
make build         # Build Docker images
make up            # Start research environment
make down          # Stop research environment
make research      # Run algorithm research
make jupyter       # Show Jupyter Lab access info
make clean         # Clean up containers and volumes
```

## 🔧 Development Workflow

### Using Cursor/VS Code
1. Open this repository in Cursor
2. Use "Remote-Containers: Reopen in Container"
3. The research code will be available in `/app/research-code/`
4. All your changes will be reflected in the container

### Using Jupyter Lab
1. Run `make up`
2. Open http://localhost:8888 in your browser
3. Navigate to the research-code directory
4. Open and run the research notebooks

### Command Line Development
1. Run `make up`
2. Connect to the container: `docker exec -it scheduling-research /bin/bash`
3. Navigate to `/app/research-code/` to access the research code

## 📁 Submodule Management

### Adding the Research Code Repository
```bash
# Add your research repository as a submodule
git submodule add <your-research-repo-url> research-code

# Initialize and update submodules
git submodule update --init --recursive
```

### Updating Research Code
```bash
# Update to latest version of research code
git submodule update --remote research-code

# Commit the submodule update
git add research-code
git commit -m "Update research code submodule"
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
- **Research Container**: Python 3.10 with all optimization libraries
- **Jupyter Lab**: Interactive development environment
- **Volume Mounting**: Live code editing from host
- **Development Tools**: All necessary packages for algorithm research

## 📊 Research Environment Features

- **Algorithm Comparison Framework**: Test and compare different scheduling algorithms
- **Test Case Management**: Create and manage test scenarios
- **Performance Visualization**: Generate charts and reports
- **Interactive Development**: Jupyter notebooks for experimentation
- **Automated Testing**: Run comprehensive algorithm evaluations

## 🔄 Workflow for Algorithm Development

1. **Develop algorithms** in the research-code repository
2. **Test locally** using the Docker environment
3. **Compare performance** using the built-in framework
4. **Visualize results** with generated charts and reports
5. **Commit changes** to the research-code repository
6. **Update submodule** in this configuration repository

## 📝 Configuration Files

- `docker-compose.yml`: Main Docker Compose configuration
- `docker/Dockerfile.research`: Research environment Docker image
- `.devcontainer/devcontainer.json`: Cursor/VS Code development container
- `scripts/setup.sh`: Automated setup script
- `Makefile`: Common commands and shortcuts

## 🤝 Contributing

1. Make changes to the research code in the research-code submodule
2. Test your changes using this configuration environment
3. Commit changes to the research-code repository
4. Update the submodule reference in this repository
5. Submit a pull request with both repository updates

## 📞 Support

For issues with:
- **Docker/Infrastructure**: Create an issue in this repository
- **Research Code/Algorithms**: Create an issue in the research-code repository