from dotenv import load_dotenv
import os
load_dotenv('token.env')
TOKEN = os.getenv('TOKEN')


HEADERS = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": f"token {TOKEN}",
}
API_URL = "https://api.github.com/search/repositories"
START_TIME = "2023-01-01T00:00:00+08:00"
END_TIME = "2024-01-01T00:00:00+08:00"
SLEEP_TIME = 1
PER_PAGE = 100
DOWNLOAD = False
INFO = ['Name', 'URL', 'Stars', 'Topics']