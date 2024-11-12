import os
from pydriller import Repository
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CommitProcessor:
    def __init__(self, repo_manager, start_date):
        self.repo_manager = repo_manager
        self.start_date = start_date
        self.repo = None
        self.repo_commits = []
        self.repo_files = []

    def collect_commits(self):
        # Inicializa o repositório se ainda não o fez
        if not self.repo:
            self.repo = self.repo_manager.get_repo()

        last_commit_date = None  # Variável para armazenar a data do último commit coletado

        for commit in Repository(self.repo_manager.repo_url, since=self.start_date).traverse_commits():
            commit_date = commit.author_date  # A data do commit

            # Se o último commit não foi coletado ainda, ou a diferença de datas for maior que 30 dias
            if last_commit_date is None or (commit_date - last_commit_date).days >= 30:
                self.repo_commits.append(commit.hash)
                last_commit_date = commit_date  # Atualiza a data do último commit

        logger.info(f"Total de commits: {len(self.repo_commits)}")

    def process_commits(self):
        if not self.repo:
            self.repo = self.repo_manager.get_repo()
        commit_count = len(self.repo_commits)
        for commit in self.repo_commits:
            self.repo.git.checkout(commit)
            logger.info(f"Commit {commit_count}/{len(self.repo_commits)}: {commit}")

            # Obtém o commit completo usando Repository novamente
            repo = Repository(self.repo_manager.repo_url)
            commit_details = next((c for c in repo.traverse_commits() if c.hash == commit), None)

            if not commit_details:
                logger.error(f'Commit {commit.hash} não encontrado.')
                commit_count -= 1
                continue

            self.repo_files = [
                os.path.relpath(os.path.join(dirpath, file), start=self.repo_manager.get_clone_path())
                for dirpath, dirnames, files in os.walk(self.repo_manager.get_clone_path())
                for file in files if file.endswith('.py')
            ]
            if len(self.repo_files) > 0:
                logger.info(f"Total de arquivos: {len(self.repo_files)}")
            
            commit_count -= 1
            yield commit_details, self.repo_files
