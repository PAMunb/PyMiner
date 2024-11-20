import logging
from datetime import datetime
import os
import csv
import ast
import gc  # Coletor de lixo

from concurrent.futures import ThreadPoolExecutor, as_completed

from commit_processor import CommitProcessor
from repo_manager import RepoManager
from visitors.underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor

# Configurando o Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_classes, start_date=datetime(2012, 1, 1), steps=30):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date, steps)
        self.feature_visitor_classes = feature_visitor_classes

    def process(self):  
        try:    
            self.repo_manager.clone_repo()
            self.commit_processor.collect_commits()

            for commit_details, repo_files in self.commit_processor.process_commits():
                commit_date = datetime.fromtimestamp(commit_details.authored_date).strftime('%Y-%m-%d')

                accumulated_results = {
                    'project': self.repo_manager.repo_name,
                    'date': commit_date,
                    'commit_hash': commit_details.hexsha,
                    'files': len(repo_files)
                }

                errors = 0

                # Cria os visitors para cada commit
                visitors = [visitor_class() for visitor_class in self.feature_visitor_classes]

                # Processa arquivos em paralelo
                with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as executor:
                    futures = {executor.submit(self.process_file, file, visitors): file for file in repo_files}
                    
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            errors += result['errors']
                            if result.get('metrics'):
                                for visitor, visitor_metrics in result['metrics'].items():
                                    for key, value in visitor_metrics.items():
                                        if isinstance(value, int):
                                            accumulated_results[key] = value
                                        elif isinstance(value, set):
                                            accumulated_results[key] = len(value)
                        except Exception as e:
                            logger.error(f"Erro ao processar arquivo {futures[future]}: {e}", exc_info=True)
                            errors += 1

                accumulated_results['errors'] = errors

                # Exporta os resultados para o CSV imediatamente
                self.export_to_csv(f"results/{self.repo_manager.repo_name}.csv", accumulated_results)

                # Libera memória usada pelos visitantes
                del visitors
                gc.collect()

        except Exception as e:
            logger.error(f'Erro ao processar o projeto {self.repo_manager.repo_name}: {e}', exc_info=True)

    def process_file(self, file, visitors):
        file_path = os.path.join(self.repo_manager.get_clone_path(), file)
        errors = 0
        visitor_errors = {}

        try:
            file_content = self._read_file(file_path)
            if not file_content:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}

            parsed_code = self._parse_code(file_content, file_path)
            if not parsed_code:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}

            for visitor in visitors:
                try:
                    if isinstance(visitor, UnderscoresNumericLiteralsVisitor):
                        visitor.set_source_code(file_content)
                    visitor.set_current_file(file)
                    visitor.visit(parsed_code)
                except Exception as visitor_error:
                    visitor_name = visitor.__class__.__name__
                    visitor_errors[visitor_name] = str(visitor_error)

            if visitor_errors:
                errors += 1

            return {
                'errors': errors,
                'visitor_errors': visitor_errors,
                'metrics': {visitor: visitor.metrics for visitor in visitors}
            }

        except Exception as e:
            return {'errors': 1, 'visitor_errors': {}, 'metrics': {}}

    def _parse_code(self, file_content, file_path):
        try:
            return ast.parse(file_content)
        except SyntaxError:
            return None

    def _read_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def export_to_csv(self, output_path, result):
        try:
            # Abre o arquivo no modo de adição
            with open(output_path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=result.keys())
                if os.path.getsize(output_path) == 0:  # Adiciona cabeçalhos apenas no início
                    writer.writeheader()
                writer.writerow(result)
        except PermissionError as e:
            logger.error(f'Erro de permissão ao criar o arquivo: {e}')
            os.remove(output_path)