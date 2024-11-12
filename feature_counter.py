import logging
import threading
import concurrent.futures
from datetime import datetime
import os
import csv
import ast

from commit_processor import CommitProcessor
from repo_manager import RepoManager

# Configurando o Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_classes, start_date=datetime(2024, 1, 1)):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date)
        self.feature_visitor_classes = feature_visitor_classes
        self.results = []

    def process(self):
        self.repo_manager.clone_repo()
        self.commit_processor.collect_commits()
        
        visitors = [visitor_class() for visitor_class in self.feature_visitor_classes]

        for commit_details, repo_files in self.commit_processor.process_commits():
            
            accumulated_results = {
                'project': self.repo_manager.repo_name,
                'date': str(commit_details.author_date.strftime('%Y-%m-%d')),
                'commit_hash': commit_details.hash,
                'files': len(repo_files)
            }
                        
            # Inicialize as métricas acumuladas para todos os visitantes
            for visitor in visitors:
                # Inicializa as métricas do visitante com zero ou conjuntos vazios
                visitor.metrics = {key: 0 if isinstance(val, int) else set()
                                            for key, val in visitor.metrics.items()}
                # Adiciona as chaves de métricas ao accumulated_results
                for key in visitor.metrics.keys():
                    accumulated_results[key] = 0

            errors = 0

            # Usando multithreading para processar os arquivos
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                futures = []
                for file in repo_files:
                    futures.append(executor.submit(self.process_file, file, visitors))
                
                # Aguarda a conclusão de todas as threads e coleta os resultados
                for future in concurrent.futures.as_completed(futures):
                    future_result = future.result()
                    errors += future_result['errors']
                    for visitor, visitor_metrics in future_result['metrics'].items():
                        for key, value in visitor_metrics.items():
                            # Verifica se o valor é um inteiro ou um set
                            if isinstance(value, int):
                                accumulated_results[key] = value  # Soma o valor diretamente
                            elif isinstance(value, set):
                                accumulated_results[key] = len(value)  # Soma o tamanho do set
                            
                            
            # Adiciona a contagem de erros ao final do dicionário accumulated_results
            accumulated_results['errors'] = errors
            # Armazena o resultado acumulado para o commit atual
            self.results.append(accumulated_results)

    def process_file(self, file, visitors):
        
        # Log indicando qual arquivo está sendo processado e qual thread está sendo usada
        logger.info(f"Thread {threading.current_thread().name} processando arquivo: {file}")
        
        file_path = os.path.join(self.repo_manager.get_clone_path(), file)
        file_metrics = {visitor: visitor.metrics.copy() for visitor in visitors}
        errors = 0
        
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
            parsed_code = ast.parse(file_content)

            for visitor in visitors:
                visitor.set_current_file(file)
                visitor.visit(parsed_code)

        except Exception as e:
            logger.error(f'Erro no arquivo {file}: {e}')
            errors += 1
        
        # Coleta as métricas após o processamento do arquivo
        result = {
            'errors': errors,
            'metrics': {visitor: visitor.metrics for visitor in visitors}
        }
        
        return result

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

        
