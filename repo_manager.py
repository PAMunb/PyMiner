import os
from pydriller import Repository
from git import Repo

class RepoManager:
    def __init__(self, repo_url, path='dataset/'):
        self.repo_url = repo_url
        self.repo_name = Repository(repo_url)._get_repo_name_from_url(repo_url)
        self.clone_path = os.path.join(path, self.repo_name)
        self.repo = None

    def clone_repo(self):
        if not os.path.exists(self.clone_path):
            self.repo = Repo.clone_from(self.repo_url, self.clone_path)
        else:
            self.repo = Repo(self.clone_path)

    def get_repo(self):
        return self.repo

    def get_clone_path(self):
        return self.clone_path
