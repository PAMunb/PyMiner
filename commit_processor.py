import os
from pydriller import Repository

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

        for commit in Repository(self.repo_manager.repo_url, since=self.start_date).traverse_commits():
            self.repo_commits.append(commit.hash)
        print("Total de commits: ", len(self.repo_commits))

    def process_commits(self):
        if not self.repo:
            self.repo = self.repo_manager.get_repo()

        for commit in self.repo_commits:
            self.repo.git.checkout(commit)
            print(f'Commit: {commit}')

            # Obtém o commit completo usando Repository novamente
            repo = Repository(self.repo_manager.repo_url)
            commit_details = next((c for c in repo.traverse_commits() if c.hash == commit), None)

            if not commit_details:
                print(f'Commit {commit.hash} não encontrado.')
                continue

            self.repo_files = [
                os.path.relpath(os.path.join(dirpath, file), start=self.repo_manager.get_clone_path())
                for dirpath, dirnames, files in os.walk(self.repo_manager.get_clone_path())
                for file in files if file.endswith('.py')
            ]
            if len(self.repo_files) > 0:
                print("Total de arquivos:", len(self.repo_files))
            
            yield commit_details, self.repo_files
