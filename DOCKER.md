# Docker Deployment Guide

This guide explains how to deploy the Anniversary Finder application using Docker.

## Prerequisites

- Docker and Docker Compose installed on your system
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Deployment Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/anniversary_finder.git
cd anniversary_finder
```

2. **Build and start the Docker container**

```bash
docker-compose up -d
```

This command builds the Docker image and starts the container in detached mode. The `-d` flag runs containers in the background.

3. **Access the application**

Open your browser and navigate to:
```
http://localhost:8989
```

## Managing the Application

### Check container status

```bash
docker-compose ps
```

### View application logs

```bash
docker-compose logs -f
```

The `-f` flag follows the log output in real-time.

### Stop the application

```bash
docker-compose down
```

### Restart the application

```bash
docker-compose restart
```

### Rebuild the application after code changes

```bash
docker-compose up -d --build
```

## Docker Compose Configuration

The `docker-compose.yml` file configures:

- Port mapping (8989:8989)
- Volume mounts for:
  - Logs directory (`./logs:/app/logs`)
  - SQLite database (`./database.db:/app/database.db`)
  - Data files (`./data:/app/data`)
- Environment variables
- Health check configuration

## Project Scripts

The project includes two Docker-specific scripts:

1. **docker-entrypoint.sh**: Used inside the Docker container to initialize the database and start the application. You don't need to run this manually.

2. **docker-manage.sh**: A helper script for managing the Docker deployment. Usage:
   ```bash
   ./docker-manage.sh start    # Start the application
   ./docker-manage.sh stop     # Stop the application
   ./docker-manage.sh status   # Check container status
   ./docker-manage.sh logs     # View logs
   ./docker-manage.sh rebuild  # Rebuild after code changes
   ```

## Customization

- To change the port mapping, edit the `ports` section in `docker-compose.yml`.
- To add environment variables, add them under the `environment` section.
- For advanced Gunicorn settings, modify the `gunicorn_config.py` file.

## Troubleshooting

- **Container fails to start**: Check logs with `docker-compose logs`
- **Database issues**: Ensure the database file exists and has proper permissions
- **Port conflicts**: If port 8989 is already in use, change the port mapping in `docker-compose.yml`
```

4. **View logs**

```bash
docker-compose logs -f
```

5. **Configure Nginx or SWAG for reverse proxy**

Use the provided `nginx_config` file as a template, but change the proxy_pass to point to your Docker container:

```
proxy_pass http://your_server_ip:8000;
```

## Managing the Docker Container

- **Stop the container**: `docker-compose down`
- **Restart the container**: `docker-compose restart`
- **Rebuild after changes**: `docker-compose up -d --build`

## Data Persistence

The Docker setup is configured to persist:

- The SQLite database file (`database.db`)
- Log files in the `logs` directory

These are mounted as volumes from your host system to the container.

## Resource Constraints (Optional)

For resource-limited environments like a home server, you may want to limit the container's resource usage in your `docker-compose.yml`:

```yaml
services:
  anniversary-app:
    # ... other settings ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

This limits the container to using at most 50% of a CPU core and 256MB of memory.
