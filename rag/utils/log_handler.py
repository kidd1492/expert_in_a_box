import logging
import os

# Ensure 'logs' directory exists
LOG_DIR = "rag/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file paths
DOC_LOG_FILE = os.path.join(LOG_DIR, "doc.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
TOOL_LOG_FILE = os.path.join(LOG_DIR, "tool.log")


# Create separate loggers
error_logger = logging.getLogger("ErrorLogger")
tool_logger = logging.getLogger("ToolLogger")
doc_logger = logging.getLogger("DocLogger")


# Set logging levels
doc_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.INFO)
tool_logger.setLevel(logging.INFO)


# Create file handlers
doc_handler = logging.FileHandler(DOC_LOG_FILE)
error_handler = logging.FileHandler(ERROR_LOG_FILE)
tool_handler = logging.FileHandler(TOOL_LOG_FILE)


# Define log format
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Attach formatters to handlers
doc_handler.setFormatter(log_format)
error_handler.setFormatter(log_format)
tool_handler.setFormatter(log_format)


# Add handlers to loggers
doc_logger.addHandler(doc_handler)
error_logger.addHandler(error_handler)
tool_logger.addHandler(tool_handler)
