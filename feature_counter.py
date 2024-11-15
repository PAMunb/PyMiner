import logging
import concurrent.futures
from datetime import datetime
import os
import csv
import ast

from commit_processor import CommitProcessor
from repo_manager import RepoManager
from visitors.underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor

# Configurando o Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_classes, start_date=datetime(2012, 1, 1), max_threads=8, steps=30):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date, steps)
        self.feature_visitor_classes = feature_visitor_classes
        self.results = []
        self.max_threads = max_threads

    def process(self):
        
        try:    
            
            self.repo_manager.clone_repo()
            self.commit_processor.collect_commits()
            
            # Criação da lista de visitors
            visitors = []
            for visitor_class in self.feature_visitor_classes:
                visitors.append(visitor_class())

            for commit_details, repo_files in self.commit_processor.process_commits():
                
                commit_date = datetime.fromtimestamp(commit_details.authored_date).strftime('%Y-%m-%d')
                
                accumulated_results = {
                    'project': self.repo_manager.repo_name,
                    'date': commit_date,
                    'commit_hash': commit_details.hexsha,
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
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                    futures = []
                    for file in repo_files:
                        futures.append(executor.submit(self.process_file, file, visitors))
                    
                    # Aguarda a conclusão de todas as threads e coleta os resultados
                    for future in concurrent.futures.as_completed(futures):
                        future_result = future.result()
                        errors += future_result['errors']
                        if future_result.get('metrics'):
                            for visitor, visitor_metrics in future_result['metrics'].items():
                                for key, value in visitor_metrics.items():
                                    if isinstance(value, int):
                                        accumulated_results[key] = value
                                    elif isinstance(value, set):
                                        accumulated_results[key] = len(value)
      
                # Adiciona a contagem de erros ao final do dicionário accumulated_results
                accumulated_results['errors'] = errors
                # Armazena o resultado acumulado para o commit atual
                self.results.append(accumulated_results)
                
        except Exception as e:
            logger.error(f'Erro ao processar o projeto {self.repo_manager.repo_name}: {e}', exc_info=True)

    def process_file(self, file, visitors):
        # Log indicando qual arquivo está sendo processado e qual thread está sendo usada
        # logger.info(f"Thread {threading.current_thread().name} processando arquivo: {file}")
        
        file_path = os.path.join(self.repo_manager.get_clone_path(), file)
        errors = 0
        visitor_errors = {}
        
        try:
            
            file_content = self._read_file(file_path)
            if not file_content:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}

            parsed_code = self._parse_code(file_content,file_path)
            if not parsed_code:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}
            
            for visitor in visitors:
                try:
                    if isinstance(visitor, UnderscoresNumericLiteralsVisitor):
                        visitor.set_source_code(file_content)
                    visitor.set_current_file(file)
                    visitor.visit(parsed_code)
                except Exception as visitor_error:
                    # Registra o erro específico do visitor sem interromper os outros
                    visitor_name = visitor.__class__.__name__
                    visitor_errors[visitor_name] = str(visitor_error)
                    # logger.error(f"Erro ao processar o visitor {visitor_name} no arquivo {file}: {visitor_error}")
            
            if len(visitor_errors) > 0:
                errors += 1

            # Coleta as métricas após o processamento do arquivo
            result = {
                'errors': errors,
                'visitor_errors': visitor_errors,  # Lista os erros por visitor
                'metrics': {visitor: visitor.metrics for visitor in visitors}
            }
            
            return result
        
        except Exception as e:
            errors += 1
            # logger.error(f'Erro ao processar arquivo {file} do projeto {self.repo_manager.repo_name}: {e}')
            return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}
    
    def _parse_code(self, file_content, file_path):
        try:
            return ast.parse(file_content)
        except SyntaxError as e:
            # logger.error(f"Falha ao analisar o código do arquivo: {file_path}: {e}")
            return None
        
    def _read_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            # logger.error(f"Conteúdo do arquivo vazio ou falha na leitura: {file_path}: {e}")
            return None  


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
            logger.error(f'Erro de permissão ao criar o arquivo: {e}')
            os.remove(output_path)

        
