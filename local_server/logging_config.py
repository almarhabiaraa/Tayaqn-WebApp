import logging
from colorlog import ColoredFormatter

# Define your log format
log_format = "%(log_color)s%(levelname)s%(reset)s:     %(log_color)s%(message)s%(reset)s"

# Create a custom logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

colors = {
    'DEBUG': 'cyan',
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Set the formatter for the handler
formatter = ColoredFormatter(log_format, log_colors=colors)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Function to get the configured logger
def get_logger():
    return logger
