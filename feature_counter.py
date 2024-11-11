from datetime import datetime
import os
import csv
import ast

from commit_processor import CommitProcessor
from repo_manager import RepoManager

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_classes, start_date=datetime(2024, 11, 10)):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date)
        self.feature_visitor_classes = feature_visitor_classes
        self.results = []

    def process(self):
        self.repo_manager.clone_repo()
        self.commit_processor.collect_commits()

        for commit_details, repo_files in self.commit_processor.process_commits():
            
            accumulated_results = {
                'project': self.repo_manager.repo_name,
                'date': str(commit_details.author_date.strftime('%Y-%m-%d')),
                'commit_hash': commit_details.hash,
                'files': len(repo_files)
            }
            
            errors = 0
            
            for visitor_class in self.feature_visitor_classes:
                visitor_instance = visitor_class()
                 
                # Inicializa as métricas do visitante para o commit atual
                visitor_instance.metrics = {key: 0 if isinstance(val, int) else set() 
                                        for key, val in visitor_instance.metrics.items()}
                
                for key, _ in visitor_instance.metrics.items():
                    accumulated_results[f'{key}'] = 0
                    
                accumulated_results['errors'] = 0

                for file in repo_files:
                    file_path = os.path.join(self.repo_manager.get_clone_path(), file)
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                        parsed_code = ast.parse(file_content)
                        
                        visitor_instance.set_current_file(file)
                        
                        visitor_instance.visit(parsed_code)
                        
                        # Acumula as métricas por arquivo
                        for key, value in visitor_instance.metrics.items():
                            if isinstance(value, int):
                                accumulated_results[key] += value
                            elif isinstance(value, set):
                                accumulated_results[key] += len(value)

                    except Exception as e:
                        print(f'Erro no arquivo {file}: {e}')
                        errors += 1  # Incrementa o contador de erros para o arquivo atual
                
                for key, value in visitor_instance.metrics.items():
                    if isinstance(value, int):
                        accumulated_results[f'{key}'] = value
                    elif isinstance(value, set):
                        accumulated_results[f'{key}'] = len(value)
            
            accumulated_results['errors'] = errors
            self.results.append(accumulated_results)

    def export_to_csv(self, output_path):
        try:
            with open(output_path, 'w', newline='') as csvfile:
                # Define os nomes das colunas para as métricas de cada visitante
                fieldnames = list(self.results[0].keys()) if self.results else []

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                # Itera sobre os resultados acumulados
                for row in self.results:
                    writer.writerow(row)

        except PermissionError as e:
            print(f"Permission Error: {e}")
            os.remove(output_path)

        
