#!/bin/bash

# Docker management script for Anniversary Finder

# Function to display help
show_help() {
  echo "Anniversary Finder Docker Management Script"
  echo "Usage: ./docker-manage.sh [command]"
  echo ""
  echo "Commands:"
  echo "  start       - Start the application"
  echo "  stop        - Stop the application"
  echo "  restart     - Restart the application"
  echo "  logs        - View application logs"
  echo "  status      - Check application status"
  echo "  rebuild     - Rebuild and restart the application"
  echo "  help        - Show this help message"
}

# Check if command was provided
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# Process command
case "$1" in
  start)
    echo "Starting Anniversary Finder..."
    docker-compose up -d
    ;;
  stop)
    echo "Stopping Anniversary Finder..."
    docker-compose down
    ;;
  restart)
    echo "Restarting Anniversary Finder..."
    docker-compose restart
    ;;
  logs)
    echo "Showing logs for Anniversary Finder..."
    docker-compose logs -f
    ;;
  status)
    echo "Status of Anniversary Finder containers:"
    docker-compose ps
    ;;
  rebuild)
    echo "Rebuilding Anniversary Finder..."
    docker-compose up -d --build
    ;;
  help)
    show_help
    ;;
  *)
    echo "Unknown command: $1"
    show_help
    exit 1
    ;;
esac
