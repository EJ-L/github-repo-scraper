import dotenv
import os
import itertools
import logging
from time_list_generation import *

dotenv.load_dotenv('token.env')
TOKEN = os.getenv("TOKEN").split(',') if os.getenv("TOKEN") else []
num_of_processes = len(TOKEN)
token_cycle = itertools.cycle(TOKEN)
time_intervals = time_list_generation(num_of_processes)

# Configure the logger to write only to a file
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawling.log")  # Logs to a file only
    ]
)

# Get a logger instance
logger = logging.getLogger(__name__)
logger.propagate = False

HEADERS = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": f"token",
}
API_URL = "https://api.github.com/search/repositories"
START_TIME = "2023-01-01T00:00:00+08:00"
END_TIME = "2024-01-01T00:00:00+08:00"
SLEEP_TIME = 1
PER_PAGE = 100
DOWNLOAD = True
INFO = ['Name', 'URL', 'Stars', 'Topics']