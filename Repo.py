import git 
import requests
from config import TOKEN, HEADERS, SLEEP_TIME, PER_PAGE
import time
from tqdm import tqdm
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

class Repository:
    def __init__(self, full_name:str, name:str, url:str, stars:str, topics:list):
        self.full_name = full_name
        self.name = name
        self.url = url
        self.stars = stars
        self.topics = topics
        self.pull_requests = []
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def clone_from_github(self) -> None:
        try:
            git.Repo.clone_from(self.url, self.full_name)
            print(f"{self.full_name} downloaded successfully")
        except Exception as e:
            print(f"Could not download file {self.full_name}")
            print(e)
            
    """Fetch the size of a GitHub repository using the GitHub API."""      
    def get_github_repo_size(full_name:str, token:str=TOKEN):
        url = f"https://api.github.com/repos/{full_name}"
        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(url, headers=headers)
        size_kb = 0
        if response.status_code == 200:
            repo_data = response.json()
            size_kb = repo_data['size']
            # print(f"The repository {full_name} size is {size_kb} KB.")
        else:
            print(f"Failed to retrieve repository info: {response.status_code} {response.reason}")
        return size_kb
    

    def fetch_modifications(self, commit_sha):
        api_url = f"https://api.github.com/repos/{self.full_name}/commits/{commit_sha}"
        response = requests.get(api_url, headers=HEADERS)

        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error: Unable to fetch commit details (Status Code: {response.status_code})")
            return

        # Parse the JSON response
        commit_data = response.json()
        files = commit_data['files']

        
        changes_list = []
        for file in files:
            changes = {
                "filename": file['filename'],
                "status": file['status'],
                "additions": file['additions'],
                "deletions": file['deletions'],
                "patch": file['patch'] if 'patch' in file else "Patch: (binary or large diff)"            
            }
            
            changes_list.append(changes)
           
        return changes_list 

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def fetch_pr(self):
        # check the name of the current Repo
        print(self.full_name)
        # count = 0 
        # find all commits with the help of pull request numbers
        for pr_num in tqdm(self.fetch_pr_generator()):
            # count += 1
            # if count > 3:
            #     print("break")
            #     break
            # avoid exceeding limit
            # time.sleep(SLEEP_TIME)
            
            # to get the commit info
            api_url = f"https://api.github.com/repos/{self.full_name}/pulls/{pr_num}/commits"
            response = requests.get(api_url, headers=HEADERS)

            # check if the response is successful
            if response.status_code != 200:
                print(f"Error: Unable to fetch pull request commits (Status Code: {response.status_code})")
                return

            # json conversion
            commits = response.json()
            
            commits_details = []
            modification_list = []
            # loop through and print each commit message
            for commit in commits:
                modification_list = self.fetch_modifications(commit['sha'])
                info = {
                    "pull_request_num": pr_num,
                    "commit sha": commit['sha'],
                    "author": commit['commit']['author']['name'],
                    "message": commit['commit']['message'],
                    "date": commit['commit']['author']['date'],
                    "modifications": modification_list
                }
                commits_details.append(info)
                    
            self.pull_requests.append(commits_details)                       
                              
    def fetch_pr_generator(self):
        pr_nums = []
        page = 1
        repo_name = self.full_name
        # search query for pr
        pr_search_query = f"is:pr repo:{repo_name}"
        api_url = f"https://api.github.com/repos/{repo_name}/pulls"  
        # look for all pr_nums
        while True:
            # time.sleep(60) # for avoiding exceeding limit within an hour
            
            # construct the request URL with pagination parameters
            query_params = {
                "q": pr_search_query,
                "state": "all",  # fetch both open and closed pull requests
                "per_page": PER_PAGE,
                "page": page
            }
                
            response = requests.get(api_url, headers=HEADERS, params=query_params)

            # check if the response is successful
            if response.status_code != 200:
                print(f"Error: Unable to fetch pull requests (Status Code: {response.status_code})")
                break

            # json format conversion
            pr_data = response.json()
                
            # If the response is empty, we've retrieved all the data
            if not pr_data:
                break
                
            for pr in pr_data:
                yield pr['number']
            # Move to the next page
            page += 1

        # self.fetch_pull_request_commits(pr_nums)