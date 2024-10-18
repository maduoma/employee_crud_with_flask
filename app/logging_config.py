import logging
from logging.handlers import RotatingFileHandler
import os

# Create a directory for logs if it doesn't exist
if not os.path.exists('logs'):
    os.mkdir('logs')

# Set up the logger
def setup_logging():
    # Define log file path and max file size (in bytes)
    log_file_path = 'logs/app.log'
    max_log_file_size = 5 * 1024 * 1024  # 5 MB

    # Configure the logging handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_file_size, backupCount=3)
    file_handler.setLevel(logging.INFO)

    # Set format for log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Add handler to the root logger
    logging.getLogger().addHandler(file_handler)

    # Set level for the root logger
    logging.getLogger().setLevel(logging.INFO)

    # Log an initial startup message
    logging.info('Logging setup complete and application has started.')

# Invoke setup_logging when imported
setup_logging()
