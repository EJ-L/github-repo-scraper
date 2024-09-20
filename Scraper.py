import requests
from Repo import Repository
from config import *
from time_handling import *
import git 
import time
from tqdm import tqdm
import pprint

class GitHubScraper:
    def __init__(self, search_query: str, api_url:str=API_URL, headers:str=HEADERS) -> None:
        self.search_query = search_query
        self.api_url = api_url
        self.headers = headers
        self.total_size_kb = 0
        
    # Fetch repositories from GitHub API
    def fetch_repositories(self, sorting_criteria:str="stars", sorting_order:str="desc", page:int=1, per_page=PER_PAGE):
        query_params = {
            "q": self.search_query,
            "sort": sorting_criteria,
            "order": sorting_order,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(self.api_url, headers=self.headers, params=query_params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None

    def fetch_paginated_repositories(self) -> list:
        responses = []
        current_page = 1
        while True:
            data = self.fetch_repositories(page=current_page)
            if data:
                responses.append(data)
            else:
                break
            print(current_page, len(data))
            current_page += 1
        return responses
    
    @staticmethod
    def forked_or_no_license(full_name:str, token=TOKEN) -> bool:
        forked = False
        no_license = False        
        
        url = f"https://api.github.com/repos/{full_name}"
        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            forked = repo_data['fork']
            print("not forked")
            if repo_data['license'] == 'null':
                no_license = True
                print("license DNE")
            # print(f"The repository {full_name} size is {size_kb} KB.")
        else:
            print(f"Failed to retrieve repository info: {response.status_code} {response.reason}")
            
        return forked or no_license

    
        
    def parse_repositories(self, repo_data: dict):
        repo = None
        for repo_item in repo_data:
            for item in repo_item:
                full_name = item['full_name']
                if not GitHubScraper.forked_or_no_license(full_name):    
                    repo = Repository(
                        full_name=full_name,
                        name=item['name'],
                        url=item['html_url'],
                        stars=item['stargazers_count'],
                        topics=item.get('topics', [])
                    )   
        
                    yield repo
