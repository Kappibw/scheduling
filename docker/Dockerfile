FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy base requirements first for better caching
COPY requirements/ requirements/

# Install base Python dependencies
RUN pip install --no-cache-dir -r requirements/simple.txt -r requirements/jupyter.txt

# Copy spacecraft scheduler submodule (must be present at build time)
COPY spacecraft_scheduler/ spacecraft_scheduler/

# Install spacecraft scheduler dependencies if they exist
RUN if [ -d "spacecraft_scheduler/requirements" ]; then \
        echo "Installing spacecraft scheduler dependencies..."; \
        for req_file in spacecraft_scheduler/requirements/*.txt; do \
            if [ -f "$req_file" ]; then \
                echo "Installing from $(basename "$req_file")..."; \
                pip install --no-cache-dir -r "$req_file"; \
            fi; \
        done; \
    else \
        echo "No spacecraft scheduler requirements found"; \
    fi

# Set Python path
ENV PYTHONPATH=/app:/app/spacecraft_scheduler

# Create directories
RUN mkdir -p /app/data /app/results /app/logs

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]