# Gunicorn configuration file for Docker deployment
import multiprocessing

# Basic configuration
bind = "0.0.0.0:8989"  # Bind to all interfaces on port 8989
workers = (
    multiprocessing.cpu_count() * 2 + 1
)  # Recommended formula for number of workers
worker_class = "sync"  # Use sync workers for simplicity
timeout = 120  # Timeout in seconds for worker processes

# Process naming
proc_name = "anniversary_app"

# Security settings
limit_request_line = 4094  # Limit request line length
limit_request_fields = 100  # Limit number of HTTP headers

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Restart workers after serving this many requests
max_requests = 1000
max_requests_jitter = 100  # Add random jitter to max_requests

# Server mechanics
daemon = False  # Don't daemonize in Docker (important!)
preload_app = True  # Preload application code for better performance
capture_output = True  # Redirect stdout/stderr to the error log

# SSL settings (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
