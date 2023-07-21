import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%d%m%Y__%H%M%S')}.log"

LOG_FILE_DIR = os.path.join(os.getcwd(), "logs")

# create folder if not available
os.makedirs(LOG_FILE_DIR, exist_ok = True)

# file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

logging.basicConfig(
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s %(message)s",
    level=logging.DEBUG,
    filename=LOG_FILE_PATH
)

# Create a console handler to print INFO level logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter to customize log messages
formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger().addHandler(console_handler)

