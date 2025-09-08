FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/ requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Set Python path
ENV PYTHONPATH=/app

# Create directories for data and results
RUN mkdir -p /app/data /app/results

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "src/main.py"]
