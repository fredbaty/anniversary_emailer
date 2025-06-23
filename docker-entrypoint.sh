#!/bin/bash

# Initialize script for Docker container
# This script will run inside the Docker container before starting Gunicorn

# Check if database exists, if not, run migration
if [ ! -f "database.db" ]; then
    echo "Database not found. Running migration..."
    cd migrations
    python csv_to_sqlite.py
    cd ..
fi

# Start the application with Gunicorn
echo "Starting the Anniversary Finder web application..."
exec gunicorn --config gunicorn_config.py wsgi:app
