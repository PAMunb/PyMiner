from datetime import datetime
import os
import csv
import ast

from commit_processor import CommitProcessor
from repo_manager import RepoManager
from feature_visitor import FeatureVisitor

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_class, start_date=datetime(2024, 8, 29)):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date)
        self.feature_visitor_class = FeatureVisitor
        self.results = []

    def process(self):
        self.repo_manager.clone_repo()
        self.commit_processor.collect_commits()

        for commit_details, repo_files in self.commit_processor.process_commits():
            feature_count = 0
            feature_while_count = 0
            error_count = 0

            for file in repo_files:
                file_path = os.path.join(self.repo_manager.get_clone_path(), file)
                try:
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    parsed_code = ast.parse(file_content)
                    
                    # Crie uma instância de FeatureVisitor e aplique a visitação
                    visitor = self.feature_visitor_class()
                    visitor.visit(parsed_code)
                    
                    # Acumula os contadores de features
                    feature_count += visitor.feature_count
                    feature_while_count += visitor.feature_while

                except Exception as e:
                    print(f'Erro no arquivo {file}: {e}')
                    error_count += 1

            # Armazena os resultados
            self.results.append({
                'project': self.repo_manager.repo_name,
                'date': str(commit_details.author_date.strftime('%Y-%m-%d')),
                'commit_hash': commit_details.hash,
                'file_count': len(repo_files),
                'feature_count': feature_count,
                'feature_while_count': feature_while_count,
                'error_count': error_count
            })

    def export_to_csv(self, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['project', 'date', 'commit_hash', 'file_count', 'feature_count', 'feature_while_count','error_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
