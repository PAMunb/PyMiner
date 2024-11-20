import os
from pydriller import Repository
from git import Repo
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class RepoManager:
    def __init__(self, repo_url, path='dataset/'):
        self.repo_url = repo_url
        self.repo_name = self.extract_repo_owner_and_name_from_url(repo_url)
        self.clone_path = os.path.join(path, self.repo_name)
        self.repo = None

    def extract_repo_owner_and_name_from_url(self,repo_url):
        try:
            # Parse a URL para obter os componentes
            path = urlparse(repo_url).path
            # Divide o caminho para obter o owner
            parts = path.strip('/').split('/')
            if len(parts) >= 2:
                return parts[0]+"_"+Repository(repo_url)._get_repo_name_from_url(repo_url)
            else:
                return Repository(repo_url)._get_repo_name_from_url(repo_url)
        except Exception as e:
            logger.error(f"Erro ao extrair owner: {str(e)}")

    def clone_repo(self):
        if not os.path.exists(self.clone_path):
            self.repo = Repo.clone_from(self.repo_url, self.clone_path)
        else:
            self.repo = Repo(self.clone_path)

    def get_repo(self):
        return self.repo

    def get_clone_path(self):
        return self.clone_path
