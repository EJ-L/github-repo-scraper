import dotenv
import os
import itertools
import logging

dotenv.load_dotenv('token.env')
TOKEN = os.getenv("TOKEN").split(',') if os.getenv("TOKEN") else []
num_of_processes = len(TOKEN)
token_cycle = itertools.cycle(TOKEN)
time_intervals = [('2023-01-01T00:00:00+08:00', '2023-03-02T20:00:00+08:00'), ('2023-03-02T20:00:00+08:00', '2023-05-02T16:00:00+08:00'), ('2023-05-02T16:00:00+08:00', '2023-07-02T12:00:00+08:00'), ('2023-07-02T12:00:00+08:00', '2023-09-01T08:00:00+08:00'), ('2023-09-01T08:00:00+08:00', '2023-11-01T04:00:00+08:00'), ('2023-11-01T04:00:00+08:00', '2024-01-01T00:00:00+08:00')]
headers_dict = {}
for idx, t in enumerate(TOKEN):
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {t}",
    }
    headers_dict[f"token {t}"] = idx
    

# Configure the logger to write only to a file
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG to capture all levels of logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawling.log")  # Logs to a file only
    ]
)

# Get a logger instance
logger = logging.getLogger(__name__)
logger.propagate = False

def get_headers():
    """Return headers with the next token in cycle."""
    token = next(token_cycle)
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}",
    }
    return headers

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