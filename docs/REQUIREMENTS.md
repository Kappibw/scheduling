# Requirements Management

This document explains how to manage Python dependencies in the submodule architecture.

## 📁 Requirements Structure

### Configuration Repository (This Repo)
```
requirements/
├── simple.txt      # Base dependencies (OR-Tools, NumPy, etc.)
└── jupyter.txt     # Jupyter-specific dependencies
```

### Research Repository (Submodule)
```
research-code/
├── requirements/
│   ├── base.txt        # Research-specific core dependencies
│   ├── research.txt    # Algorithm-specific dependencies
│   ├── visualization.txt # Visualization dependencies
│   └── testing.txt     # Testing dependencies
├── src/
├── tests/
└── notebooks/
```

## 🔧 How It Works

### 1. **Base Dependencies (Configuration Repo)**
The configuration repository provides the foundation:
- **Python 3.10** with system dependencies
- **Core libraries**: NumPy, Pandas, SciPy, OR-Tools
- **Jupyter Lab**: Interactive development environment
- **Basic utilities**: Click, PyYAML, etc.

### 2. **Research Dependencies (Submodule)**
Your research repository adds specific dependencies:
- **Algorithm libraries**: CVXPY, Gurobi, etc.
- **Research tools**: Specific optimization libraries
- **Visualization**: Additional plotting libraries
- **Testing**: Research-specific testing tools

### 3. **Installation Process**
1. **Build time**: Base dependencies are installed
2. **Runtime**: Research dependencies are installed when container starts
3. **Automatic**: The entrypoint script handles research requirements

## 📝 Setting Up Your Research Repository

### Step 1: Create Requirements Directory
```bash
# In your research repository
mkdir requirements
```

### Step 2: Create Requirements Files

#### `requirements/base.txt` (Research-specific core)
```txt
# Research-specific core dependencies
# These are in addition to the base dependencies from config repo

# Additional optimization libraries
cvxpy>=1.3.0
gurobipy>=10.0.0  # If you have Gurobi license

# Additional data handling
networkx>=3.0
scikit-learn>=1.3.0

# Additional utilities
joblib>=1.3.0
```

#### `requirements/research.txt` (Algorithm-specific)
```txt
# Algorithm-specific dependencies
# Include any specialized libraries for your algorithms

# Example: Additional MILP solvers
cplex>=22.1.0  # If you have CPLEX license

# Example: Machine learning for scheduling
torch>=2.0.0
tensorflow>=2.13.0

# Example: Evolutionary algorithms
deap>=1.4.0
```

#### `requirements/visualization.txt` (Visualization)
```txt
# Additional visualization libraries
bokeh>=3.0.0
dash>=2.14.0
streamlit>=1.28.0

# 3D visualization
plotly>=5.15.0
mayavi>=4.8.0
```

#### `requirements/testing.txt` (Testing)
```txt
# Research-specific testing tools
pytest-benchmark>=4.0.0
pytest-cov>=4.1.0
hypothesis>=6.82.0

# Performance testing
memory-profiler>=0.61.0
line-profiler>=4.1.0
```

### Step 3: Test Installation
```bash
# In your research repository
pip install -r requirements/base.txt
pip install -r requirements/research.txt
# etc.
```

## 🚀 Usage Examples

### Example 1: Simple Research Repository
```
research-code/
├── requirements/
│   └── base.txt        # Just basic research dependencies
├── src/
└── tests/
```

### Example 2: Complex Research Repository
```
research-code/
├── requirements/
│   ├── base.txt        # Core research dependencies
│   ├── milp.txt        # MILP-specific dependencies
│   ├── ml.txt          # Machine learning dependencies
│   ├── visualization.txt # Visualization dependencies
│   └── testing.txt     # Testing dependencies
├── src/
├── tests/
└── notebooks/
```

## 🔄 Development Workflow

### 1. **Add New Dependencies**
```bash
# In your research repository
echo "new-library>=1.0.0" >> requirements/research.txt
git add requirements/research.txt
git commit -m "Add new-library dependency"
git push
```

### 2. **Update Configuration Repository**
```bash
# In the configuration repository
git submodule update --remote research-code
git add research-code
git commit -m "Update research code with new dependencies"
```

### 3. **Rebuild Container**
```bash
# In the configuration repository
make build
make up
```

## 🐳 Docker Integration

### Automatic Installation
The container automatically installs research requirements when it starts:

```bash
# Container startup process:
1. Install base dependencies (from config repo)
2. Mount research-code submodule
3. Install research dependencies (from submodule)
4. Start Jupyter Lab
```

### Manual Installation
You can also install requirements manually:

```bash
# Connect to running container
docker exec -it scheduling-research /bin/bash

# Install specific requirements
pip install -r /app/research-code/requirements/research.txt

# Or install all research requirements
/usr/local/bin/install-research-requirements.sh
```

## 📋 Best Practices

### 1. **Keep Base Dependencies Minimal**
- Only include truly essential dependencies in the config repo
- Let research repositories add specialized dependencies

### 2. **Use Specific Versions**
```txt
# Good: Specific versions
numpy==1.24.3
pandas==2.0.3

# Avoid: Loose versions (unless necessary)
numpy>=1.24.0
pandas>=2.0.0
```

### 3. **Organize by Purpose**
```txt
# requirements/base.txt - Core research dependencies
# requirements/algorithms.txt - Algorithm-specific dependencies
# requirements/visualization.txt - Visualization dependencies
# requirements/testing.txt - Testing dependencies
```

### 4. **Document Dependencies**
```txt
# requirements/research.txt
# Research-specific dependencies for robot scheduling algorithms

# MILP solvers
cvxpy>=1.3.0
gurobipy>=10.0.0  # Requires Gurobi license

# Machine learning
scikit-learn>=1.3.0
```

## 🔧 Troubleshooting

### Dependencies Not Installing
```bash
# Check if requirements directory exists
ls -la /app/research-code/requirements/

# Check container logs
docker-compose logs research

# Install manually
docker exec -it scheduling-research /usr/local/bin/install-research-requirements.sh
```

### Version Conflicts
```bash
# Check installed packages
docker exec -it scheduling-research pip list

# Check for conflicts
docker exec -it scheduling-research pip check
```

### Missing Dependencies
```bash
# Add to appropriate requirements file in research repository
echo "missing-package>=1.0.0" >> requirements/research.txt

# Rebuild container
make build
make up
```

## 📊 Example Research Repository Structure

```
your-research-repo/
├── requirements/
│   ├── base.txt           # Core research dependencies
│   ├── milp.txt           # MILP solver dependencies
│   ├── ml.txt             # Machine learning dependencies
│   ├── visualization.txt  # Visualization dependencies
│   └── testing.txt        # Testing dependencies
├── src/
│   ├── algorithms/
│   │   ├── milp/          # MILP algorithms
│   │   ├── ml/            # ML algorithms
│   │   └── heuristic/     # Heuristic algorithms
│   ├── common/
│   └── visualization/
├── tests/
├── notebooks/
└── research.py
```

This structure allows you to:
- **Modularize dependencies** by purpose
- **Easily add new algorithms** with their specific requirements
- **Maintain clean separation** between different types of dependencies
- **Enable selective installation** of only needed dependencies
