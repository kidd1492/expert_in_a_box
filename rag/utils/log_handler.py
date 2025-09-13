import logging
import os

# Ensure 'logs' directory exists
LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file paths
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
PROJECT_LOG_FILE = os.path.join(LOG_DIR, "project.log")

# Create separate loggers
app_logger = logging.getLogger("AppLogger")
project_logger = logging.getLogger("ProjectLogger")

# Set logging levels
app_logger.setLevel(logging.INFO)
project_logger.setLevel(logging.INFO)

# Create file handlers
app_handler = logging.FileHandler(APP_LOG_FILE)
project_handler = logging.FileHandler(PROJECT_LOG_FILE)

# Define log format
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Attach formatters to handlers
app_handler.setFormatter(log_format)
project_handler.setFormatter(log_format)

# Add handlers to loggers
app_logger.addHandler(app_handler)
project_logger.addHandler(project_handler)