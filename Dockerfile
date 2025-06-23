FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Expose the port Gunicorn will listen on
EXPOSE 8989

# Use our custom entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
