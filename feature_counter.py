from datetime import datetime, timezone
import os
import csv
import ast

from commit_processor import CommitProcessor
from repo_manager import RepoManager
from feature_visitor import FeatureVisitor

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_class, start_date=datetime(2024, 11, 1)):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date)
        self.feature_visitor_class = feature_visitor_class
        self.results = []

    def process(self):
        self.repo_manager.clone_repo()
        self.commit_processor.collect_commits()

        for commit_details, repo_files in self.commit_processor.process_commits():
            type_hint_list = 0
            type_hint_tuple = 0
            type_hint_dict = 0
            type_hint_set = 0
            type_hint_frozenset = 0
            type_hint_type = 0
            type_hint_file_list = 0
            type_hint_file_tuple = 0
            type_hint_file_dict = 0
            type_hint_file_set = 0
            type_hint_file_frozenset = 0
            type_hint_file_type = 0
            error_count = 0

            for file in repo_files:
                file_path = os.path.join(self.repo_manager.get_clone_path(), file)
                try:
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    parsed_code = ast.parse(file_content)
                    
                    # Crie uma instância de FeatureVisitor e aplique a visitação
                    visitor = self.feature_visitor_class()
                    
                    visitor.set_current_file(file)
                    
                    visitor.visit(parsed_code)
                    
                    type_hint_list += visitor.type_hint_counts['list']
                    type_hint_tuple += visitor.type_hint_counts['tuple']
                    type_hint_dict += visitor.type_hint_counts['dict']
                    type_hint_set += visitor.type_hint_counts['set']
                    type_hint_frozenset += visitor.type_hint_counts['frozenset']
                    type_hint_type += visitor.type_hint_counts['type']
                    
                    type_hint_file_list += len(visitor.type_hint_file_counts['list'])
                    type_hint_file_tuple += len(visitor.type_hint_file_counts['tuple'])
                    type_hint_file_dict += len(visitor.type_hint_file_counts['dict'])
                    type_hint_file_set += len(visitor.type_hint_file_counts['set'])
                    type_hint_file_frozenset += len(visitor.type_hint_file_counts['frozenset'])
                    type_hint_file_type += len(visitor.type_hint_file_counts['type'])

                except Exception as e:
                    print(f'Erro no arquivo {file}: {e}')
                    error_count += 1

            # Armazena os resultados
            self.results.append({
                'project': self.repo_manager.repo_name,
                'date': str(commit_details.author_date.strftime('%Y-%m-%d')),
                'commit_hash': commit_details.hash,
                'file_count': len(repo_files),
                'type_hint_list': type_hint_list,
                'type_hint_tuple': type_hint_tuple,
                'type_hint_dict': type_hint_dict,
                'type_hint_set': type_hint_set,
                'type_hint_frozenset': type_hint_frozenset,
                'type_hint_type': type_hint_type,
                'type_hint_file_list': type_hint_file_list,
                'type_hint_file_tuple': type_hint_file_tuple,
                'type_hint_file_dict': type_hint_file_dict,
                'type_hint_file_set': type_hint_file_set,
                'type_hint_file_frozenset': type_hint_file_frozenset,
                'type_hint_file_type': type_hint_file_type,
                'error_count': error_count
            })

    def export_to_csv(self, output_path):
        try:
            with open(output_path, 'w', newline='') as csvfile:
                fieldnames = ['project', 'date', 'commit_hash', 'file_count',
                               'type_hint_list','type_hint_tuple','type_hint_dict','type_hint_set','type_hint_frozenset','type_hint_type',
                               'type_hint_file_list','type_hint_file_tuple','type_hint_file_dict','type_hint_file_set','type_hint_file_frozenset','type_hint_file_type','error_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in self.results:
                    writer.writerow(row) 

        except PermissionError as e:
            print(f"Permission Error: {e} ")
            os.remove(output_path)

        
