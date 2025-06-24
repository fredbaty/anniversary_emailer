#!/bin/bash

# Initialize script for Docker container
# This script will run inside the Docker container before starting Gunicorn

# Start the application with Gunicorn
echo "Starting the Anniversary Finder web application..."
exec gunicorn --config gunicorn_config.py wsgi:app
