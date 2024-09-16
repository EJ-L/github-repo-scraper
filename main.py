from time_handling import *
from config import PER_PAGE, START_TIME, END_TIME, DOWNLOAD
from writers import *
from Scraper import GitHubScraper
import time

def main():
    # repositories = []
    current_time = START_TIME
    size = 0
    count = 0
    # define the writer according to desired file format
    csv_writer = CSVWriter(file_name=f'github_repos_{START_TIME[0:4]}.csv')  # For CSV
    json_writer = JSONWriter(file_name=f'github_repos_{START_TIME[0:4]}.json')
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
            count += 1
            if count > 3:
                break
            # download the repo
            if DOWNLOAD:
                print("downloading")
                repo.clone_from_github()
            # get the pull requests
            repo.fetch_pr()
            # write to the csv
            csv_writer.write(repo)
            # write to the jsonl
            json_writer.write(repo)
    
        print(f"Successfully written {count} repositories.")
        # sleep for 3s for avoiding exceeding the search query limit
        time.sleep(3)
    json_writer.close()
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