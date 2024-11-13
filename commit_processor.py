import os
from pydriller import Repository
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CommitProcessor:
    def __init__(self, repo_manager, start_date, steps):
        self.repo_manager = repo_manager
        self.start_date = start_date
        self.repo = None
        self.repo_commits = []
        self.repo_files = []
        self.steps = steps

    def collect_commits(self):
        # Inicializa o repositório se ainda não o fez
        if not self.repo:
            self.repo = self.repo_manager.get_repo()

        last_commit_date = None  # Variável para armazenar a data do último commit coletado

        for commit in Repository(self.repo_manager.repo_url, since=self.start_date).traverse_commits():
            commit_date = commit.author_date  # A data do commit

            # Se o último commit não foi coletado ainda, ou a diferença de datas for maior que 30 dias
            if last_commit_date is None or (commit_date - last_commit_date).days >= self.steps:
                self.repo_commits.append(commit.hash)
                last_commit_date = commit_date  # Atualiza a data do último commit

        logger.info(f"Total de commits: {len(self.repo_commits)}")
        
    def should_ignore_file(self, file_path):
        ignored_files = [
            '__init__.py', 'setup.py'
        ]
        ignored_dirs = [
            'venv', 'env', '__pycache__', 'dist', 'build', 'site-packages', 'node_modules'
        ]
        # Verificar se é um arquivo ou diretório ignorado
        file_name = os.path.basename(file_path)
        dir_name = os.path.basename(os.path.dirname(file_path))

        return file_name in ignored_files or dir_name in ignored_dirs

    def process_commits(self):
        if not self.repo:
            self.repo = self.repo_manager.get_repo()
        commit_count = len(self.repo_commits)
        for commit in self.repo_commits:
            self.repo.git.checkout(commit)
            logger.info(f"Commit {commit_count}/{len(self.repo_commits)}: {commit}")

            # Obtém o commit completo usando Repository novamente
            commit_details = self.get_commit_by_hash(self.repo_manager.repo_url, commit)

            if not commit_details:
                logger.error(f'Commit {commit.hash} não encontrado.')
                commit_count -= 1
                continue

            # Filtra arquivos que não devem ser analisados
            self.repo_files = [
                os.path.relpath(os.path.join(dirpath, file), start=self.repo_manager.get_clone_path())
                for dirpath, dirnames, files in os.walk(self.repo_manager.get_clone_path())
                for file in files if file.endswith('.py') and not self.should_ignore_file(os.path.join(dirpath, file))
            ]

            if len(self.repo_files) > 0:
                logger.info(f"Total de arquivos: {len(self.repo_files)}")
            
            commit_count -= 1
            yield commit_details, self.repo_files
            
    def get_commit_by_hash(self, repo_url, commit_hash):
        repo = Repository(repo_url)
        # Utilize traverse_commits(), mas pare assim que encontrar o commit
        for commit in repo.traverse_commits():
            if commit.hash == commit_hash:
                return commit
        return None