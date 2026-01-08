# Use Python 3.11 slim image (has good pyswisseph wheel support)
FROM python:3.11-slim

# Install build dependencies for pyswisseph C extension
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy PyJHora library first (needed for PYTHONPATH)
COPY PyJHora/src /app/PyJHora/src

# Copy backend requirements and install
COPY web-app/backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY web-app/backend /app/backend

# Set environment variables
ENV PYTHONPATH=/app/PyJHora/src
ENV ENVIRONMENT=production

# Expose port (Render provides $PORT)
EXPOSE 10000

# Start the application
CMD cd /app/backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
