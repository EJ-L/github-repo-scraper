from time_handling import *
from config import *
from writers import *
from Scraper import GitHubScraper
import time
import os
import multiprocessing
from multiprocessing import Pool, Lock
import requests

lock = Lock()


REPO_DATA_DIR = "repo_data"
REPO_DIR = "repo"
INDEX_FILE_PATH = os.path.join(REPO_DATA_DIR, "index.jsonl")
DOWNLOAD = False

# Function to ensure the repo_data directory exists
def ensure_repo_data_dir_exists():
    if not os.path.exists(REPO_DATA_DIR):
        os.makedirs(REPO_DATA_DIR)
        
def ensure_repo_dir_exists():
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
        
def read_json_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except:
        data = []
    return data

def read_jsonl_file(filename):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = json.loads(line)
                data.append(line)
    except:
        data = []
    print(data)
    return data

def main(time_interval, token):
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}",
    }
    # repositories = []
    ensure_repo_data_dir_exists()
    ensure_repo_dir_exists()
    current_time = time_interval[0]
    end_time = time_interval[1]
    print(time_interval)
    # size = 0
    count = 0
    # define the writer according to desired file format
    # csv_writer = CSVWriter(file_name=f'repo_data/index.csv')  # For CSV
    data = read_jsonl_file(INDEX_FILE_PATH)
    # headers = get_headers()

    while time_smaller_than(current_time, end_time):
        # print the current time
        print(current_time)
        # define the query: get the next period by a desired time interval
        repo_search_query = get_next_period(current_time, end_time, extra_hour=120, extra_min=0, extra_sec=0)
        # change the current time to the next desired hour
        current_time = next_hour(current_time, end_time, extra_hour=120, extra_min=0, extra_sec=0)
        logger.info(f"worker id: {token} -- repo_search_query: {repo_search_query}")
        print(repo_search_query)
        # initialize scraper

        scraper = GitHubScraper(search_query=repo_search_query, headers=headers)

        # repo_data: a list of Repo() object
        repo_data = scraper.fetch_paginated_repositories()
        repo_data = scraper.parse_repositories(repo_data)
        for repo in repo_data:
            json_writer = JSONWriter(file_name=f'repo_data/{repo.name}.json')
            count += 1
            # if count > 3:
            #     break
            # download the repo
            read = False
            if DOWNLOAD:
                repo.clone_from_github()
            # get the pull requests
            for line in data:
                if line['full_name'] == repo.full_name:
                    print("repo already written")
                    read = True
                    break
                
            if read:
                continue
            
            data.append(
                {
                    "full_name": repo.full_name,
                    "directory": f"repo/{repo.name}",
                    "json_location": f"repo_data/{repo.name}.json",
                    "creation_date": repo.creation_date,
                    "stars": repo.stars,
                    "repo_topics": repo.topics
                }
            )
            with lock:
                with open(INDEX_FILE_PATH, "a") as f:
                    for entry in data:
                        json.dump(entry, f)
                        f.write('\n')
                        logger.info("write to index.jsonl")
            repo.fetch_pr()
            time.sleep(3)
            # write to the csv
            # csv_writer.write(repo)
            # write to the jsonl
            json_writer.write(repo)
            logger.info(f"write {repo.full_name} data")
    
        print(f"Successfully written {count} repositories.")


if __name__ == "__main__":
    with Pool(num_of_processes) as pool:
        tasks = [(time_interval, token) for time_interval, token in zip(time_intervals, itertools.cycle(TOKEN))]
        pool.starmap(main, tasks)