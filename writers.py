import csv
import json
from abc import ABC, abstractmethod
from config import INFO
from Repo import Repository

""" Base class for writers """
class RepoWriter(ABC):
    @abstractmethod
    def write(self, repositories):
        pass

""" CSVWriter which writes data to csv """
class CSVWriter(RepoWriter):
    def __init__(self, file_name: str):
        self.file_name = file_name
        with open(self.file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(INFO)
            
    # write repository info to a CSV file
    def write(self, repo: Repository):
        with open(self.file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # write
            writer.writerow([repo.full_name, repo.url, repo.stars, ', '.join(repo.topics)])

""" JSONWriter which writes data to json format """
class JSONWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.first_item = True
        self.file = open(self.file_name, 'a', encoding='utf-8')
        # self.file.write('[')  # Start the JSON array

    def write(self, repo):
        if not self.first_item:
            self.file.write(',')
        else:
            self.first_item = False
        json_data = {
            "full_name": repo.full_name,
            "url": repo.url,
            "stars": repo.stars,
            "topics": repo.topics,
            "creation_date": repo.creation_date,
            "pull_requests": repo.pull_requests
        }
        json.dump(json_data, self.file, indent=4)

    def close(self):
        self.file.write(']')  # End the JSON array
        self.file.close()