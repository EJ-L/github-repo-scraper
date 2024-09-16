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
        
    def parse_repositories(self, repo_data: dict):
        repo = None
        for repo_item in repo_data:
            for item in repo_item:
                repo = Repository(
                    full_name=item['full_name'],
                    name=item['name'],
                    url=item['html_url'],
                    stars=item['stargazers_count'],
                    topics=item.get('topics', [])
                )   
        
                yield repo
