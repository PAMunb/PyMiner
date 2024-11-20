import os
from pydriller import Repository
from datetime import datetime, timedelta
import logging
from git import Repo

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
        
        try:
            for commit in Repository(self.repo_manager.repo_url, since=self.start_date).traverse_commits():
                commit_date = commit.author_date

                # Se o último commit não foi coletado ainda, ou a diferença de datas for maior que 30 dias
                if last_commit_date is None or (commit_date - last_commit_date).days >= self.steps:
                    self.repo_commits.append(commit.hash)
                    last_commit_date = commit_date
            
        except Exception as e:
            logger.error(f"Erro ao coletar os commits do repositório {self.repo_manager.repo_name}: {str(e)}")
        
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
        
        logger.info(f"Total de commits: {commit_count}")
        
        for commit in self.repo_commits:
            try:
                
                self.repo.git.checkout(commit)

                # Obtém o commit completo usando Repository novamente
                commit_details = self.get_commit_by_hash(commit)

                if not commit_details:
                    # logger.error(f'Commit {commit.hash} não encontrado.')
                    commit_count -= 1
                    continue

                # Filtra arquivos que não devem ser analisados
                self.repo_files = [
                    os.path.relpath(os.path.join(dirpath, file), start=self.repo_manager.get_clone_path())
                    for dirpath, dirnames, files in os.walk(self.repo_manager.get_clone_path())
                    for file in files if file.endswith('.py') and not self.should_ignore_file(os.path.join(dirpath, file))
                ]

                if len(self.repo_files) > 0:
                    commit_date = datetime.fromtimestamp(commit_details.authored_date).strftime('%Y-%m-%d')
                    
                    logger.info(f"Commit {commit_count}/{len(self.repo_commits)}: hash:{ commit} | date:{ commit_date} from {self.repo_manager.repo_name} | Total de arquivos: {len(self.repo_files)}")
                
                commit_count -= 1
                yield commit_details, self.repo_files
            except Exception as e:
                # Registrar a exceção no log e continuar com o próximo commit
                logger.error(f"Erro ao processar commit {commit.hash}: {str(e)}")
                commit_count -= 1
                continue
    
    def get_commit_by_hash(self, commit_hash):
        try:

            repo = Repo(self.repo_manager.get_clone_path())

            commit = repo.commit(commit_hash)

            return commit
        except KeyError:
            logger.error(f"Commit {commit_hash} não encontrado.")
            return None
        except Exception as e:
            logger.error(f"Erro ao acessar o repositório: {str(e)}")
            return None