# Spacecraft Scheduler Configuration

This repository contains the Docker configuration and infrastructure setup for the spacecraft scheduler development environment. The actual scheduler code is managed in a separate repository and linked via git submodules.

## 🏗️ Repository Structure

```
spacecraft_scheduler_config/
├── docker/
│   └── Dockerfile              # Single Dockerfile for everything
├── .devcontainer/
│   └── devcontainer.json       # Cursor/VS Code development container config
├── scripts/
│   └── add-spacecraft-scheduler.sh  # Helper script to add submodule
├── spacecraft_scheduler/       # Git submodule (main scheduler repository)
├── data/                       # Persistent data directory
├── results/                    # Persistent results directory
├── logs/                       # Persistent logs directory
├── requirements/               # Base Python dependencies
├── docker-compose.yml          # Docker Compose configuration
└── Makefile                    # Common commands
```

## 🚀 Quick Setup (5 Minutes)

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone This Repository
```bash
git clone <this-config-repo-url>
cd spacecraft_scheduler_config
```

### 2. Add Your Spacecraft Scheduler Repository as a Submodule
```bash
# Using the helper script (recommended)
./scripts/add-spacecraft-scheduler.sh <spacecraft-scheduler-repo-url>

# Or manually
git submodule add <spacecraft-scheduler-repo-url> spacecraft_scheduler
```

### 3. Build and Start the Development Environment
```bash
make build
make up
```

### 4. Access the Environment
- **Jupyter Lab**: http://localhost:8888
- **Cursor Dev Container**: Use "Remote-Containers: Reopen in Container"

## 🔧 Available Commands

```bash
make help          # Show all available commands
make build         # Build Docker image with spacecraft scheduler dependencies
make up            # Start development environment
make down          # Stop development environment
make clean         # Clean up containers and volumes
make jupyter       # Show Jupyter Lab access info
```

## 💻 Development Workflow

### Option 1: Using Cursor/VS Code Dev Container (Recommended)

1. **Open this repository in Cursor**
2. **Reopen in Container**: 
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Remote-Containers: Reopen in Container"
   - Select it and wait for the container to build and start
3. **Your spacecraft scheduler code** will be available in `/app/spacecraft_scheduler/`
4. **Make changes** directly in the container - they'll be reflected on your host
5. **All dependencies** are pre-installed and ready to use

### Option 2: Using Jupyter Lab

1. **Start the environment**:
   ```bash
   make up
   ```
2. **Open Jupyter Lab**: http://localhost:8888
3. **Navigate to** the `spacecraft_scheduler/` directory
4. **Develop in notebooks** or create new Python files
5. **No password required** for development

### Option 3: Command Line Development

1. **Start the environment**:
   ```bash
   make up
   ```
2. **Connect to the container**:
   ```bash
   docker exec -it spacecraft-scheduler-dev /bin/bash
   ```
3. **Navigate to** `/app/spacecraft_scheduler/` to access your scheduler code
4. **Run Python scripts** directly in the container

## 📁 Working with Submodules

### Adding the Spacecraft Scheduler Repository
```bash
# Using the helper script (recommended)
./scripts/add-spacecraft-scheduler.sh <spacecraft-scheduler-repo-url>

# Or manually
git submodule add <spacecraft-scheduler-repo-url> spacecraft_scheduler
```

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

## 📊 Persistent Data

The following directories persist across container restarts:
- `data/` - Input data files
- `results/` - Generated results and outputs  
- `logs/` - Application logs

These directories are owned by the configuration repository and shared with the spacecraft scheduler submodule.

## 🔄 Complete Development Workflow

1. **Clone this configuration repository**
2. **Add your spacecraft scheduler repository as a submodule**
3. **Build the Docker environment**: `make build`
4. **Start the environment**: `make up`
5. **Open in Cursor dev container** or use Jupyter Lab
6. **Develop your algorithms** in the spacecraft_scheduler directory
7. **Test and iterate** using the containerized environment
8. **Commit changes** to the spacecraft scheduler repository
9. **Update submodule reference** in this configuration repository

## 🆘 Troubleshooting

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
# Rebuild container (dependencies are installed at build time)
make build
```

### Dev Container Not Working
1. **Check Docker is running**
2. **Try rebuilding**: `make clean && make build`
3. **Restart Cursor/VS Code**
4. **Check .devcontainer/devcontainer.json** is correct

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