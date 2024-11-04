from time_handling import *
from config import PER_PAGE, START_TIME, END_TIME, DOWNLOAD
from writers import *
from Scraper import GitHubScraper
import time
import os

REPO_DATA_DIR = "repo_data"
REPO_DIR = "repo"
INDEX_FILE_PATH = os.path.join(REPO_DATA_DIR, "index.json")

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
    

def main():
    # repositories = []
    ensure_repo_data_dir_exists()
    ensure_repo_dir_exists()
    current_time = START_TIME
    # size = 0
    count = 0
    # define the writer according to desired file format
    # csv_writer = CSVWriter(file_name=f'repo_data/index.csv')  # For CSV
    data = read_json_file(INDEX_FILE_PATH)
    while time_smaller_than(current_time, END_TIME):
        # print the current time
        print(current_time)
        # define the query: get the next period by a desired time interval
        repo_search_query = get_next_period(current_time, END_TIME, extra_hour=120, extra_min=0, extra_sec=0)
        # change the current time to the next desired hour
        current_time = next_hour(current_time, END_TIME, extra_hour=120, extra_min=0, extra_sec=0)
        print(repo_search_query)
        # initialize scraper
        scraper = GitHubScraper(search_query=repo_search_query)

        # repo_data: a list of Repo() object
        repo_data = scraper.fetch_paginated_repositories()
        repo_data = scraper.parse_repositories(repo_data)
        # iterate through a generator
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
                    "json_location": f"repo_data/{repo.name}.json"
                }
            )
            
            with open(INDEX_FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)
                
            repo.fetch_pr()
            time.sleep(3)
            # write to the csv
            # csv_writer.write(repo)
            # write to the jsonl
            json_writer.write(repo)
    
        print(f"Successfully written {count} repositories.")
        # sleep for 3s for avoiding exceeding the search query limit
    # json_writer.close()
    #     # estimate the size of the scrapped repos
    #     size += scraper.total_size_kb
        
    #     repositories.append(current_repo)
    #     # time.sleep(SLEEP_TIME)
    #     print(f"{size / 1024 / 1024} GB")
    # writer = JSONWriter(file_name=f'github_repos_{START_TIME[0:4]}.json')  # For CSV

    #     # writer = JSONWriter(file_name='github_repos.json')  # For JSON
    # writer.write(repositories)


if __name__ == "__main__":
    main()