import logging
from datetime import datetime
import os
import csv
import ast
import gc

from concurrent.futures import ThreadPoolExecutor, as_completed

from commit_processor import CommitProcessor
from repo_manager import RepoManager
from visitors.underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor

# Configurando o Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureCounter:
    def __init__(self, repo_url, feature_visitor_classes, start_date=datetime(2008, 1, 1), end_date=datetime(2024, 12, 31), steps=30):
        self.repo_manager = RepoManager(repo_url)
        self.commit_processor = CommitProcessor(self.repo_manager, start_date, end_date, steps)
        self.feature_visitor_classes = feature_visitor_classes

    def process(self):  
        try:    
            self.repo_manager.clone_repo()
            self.commit_processor.collect_commits()

            for commit_details, repo_files in self.commit_processor.process_commits():
                commit_hash = commit_details.hexsha
                commit_date = datetime.fromtimestamp(commit_details.authored_date).strftime('%Y-%m-%d')

                accumulated_results = {
                    'project': self.repo_manager.repo_name,
                    'date': commit_date,
                    'commit_hash': commit_hash,
                    'files': len(repo_files)
                }

                errors = 0
                visitors_instances = []

                with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as executor:
                    futures = {
                        executor.submit(self.process_file, file, self.feature_visitor_classes, commit_hash): file 
                        for file in repo_files
                    }
                    
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            errors += result['errors']

                            # Coleta as métricas de todos os visitors desse arquivo
                            for visitor_name, visitor_metrics in result.get('metrics', {}).items():
                                # Acumula métricas no accumulated_results
                                for key, value in visitor_metrics.items():
                                    if isinstance(value, int):
                                        accumulated_results[key] = accumulated_results.get(key, 0) + value
                                    elif isinstance(value, set):
                                        if key not in accumulated_results:
                                            accumulated_results[key] = set()
                                        accumulated_results[key].update(value)

                            # Guarda instâncias dos visitors para depois extrair os matches
                            if 'visitors_instances' in result:
                                visitors_instances.extend(result['visitors_instances'])

                        except Exception as e:
                            logger.error(f"Erro ao processar arquivo {futures[future]}: {e}", exc_info=True)
                            errors += 1

                # Converte sets para tamanho para salvar no CSV de métricas
                for k, v in accumulated_results.items():
                    if isinstance(v, set):
                        accumulated_results[k] = len(v)

                accumulated_results['errors'] = errors

                # Salva CSV geral de métricas
                self.export_to_csv(f"results/{self.repo_manager.repo_name}.csv", accumulated_results)

                # Extrai todos os matches de StructuralPatternMatchingVisitor para CSV separado
                all_matches = []
                for visitor in visitors_instances:
                    if hasattr(visitor, 'matches_found'):
                        all_matches.extend(visitor.matches_found)

                self.export_matches_to_csv(f"results/{self.repo_manager.repo_name}_matches.csv", all_matches)

                gc.collect()

        except Exception as e:
            logger.error(f'Erro ao processar o projeto {self.repo_manager.repo_name}: {e}', exc_info=True)

    def process_file(self, file, visitor_classes, commit_hash):
        file_path = os.path.join(self.repo_manager.get_clone_path(), file)
        errors = 0
        visitor_errors = {}
        metrics = {}
        visitors_instances = []

        try:
            file_content = self._read_file(file_path)
            if not file_content:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}, 'visitors_instances': []}

            parsed_code = self._parse_code(file_content, file_path)
            if not parsed_code:
                return {'errors': 1, 'visitor_errors': {}, 'metrics': {}, 'visitors_instances': []}

            for visitor_class in visitor_classes:
                try:
                    if visitor_class.__name__ == 'StructuralPatternMatchingVisitor':
                        visitor = visitor_class(file_content)
                        visitor.set_current_file(file)
                        visitor.set_current_commit(commit_hash)
                    else:
                        visitor = visitor_class()
                        if hasattr(visitor, 'set_source_code'):
                            visitor.set_source_code(file_content)
                        if hasattr(visitor, 'set_current_file'):
                            visitor.set_current_file(file)
                        if hasattr(visitor, 'set_current_commit'):
                            visitor.set_current_commit(commit_hash)

                    visitor.visit(parsed_code)
                    visitors_instances.append(visitor)
                except Exception as ve:
                    visitor_errors[visitor_class.__name__] = str(ve)
                    errors += 1

            for v in visitors_instances:
                metrics[v.__class__.__name__] = v.metrics

            return {
                'errors': errors,
                'visitor_errors': visitor_errors,
                'metrics': metrics,
                'visitors_instances': visitors_instances
            }

        except Exception as e:
            logger.error(f"Erro no processamento do arquivo {file_path}: {e}", exc_info=True)
            return {'errors': 1, 'visitor_errors': {}, 'metrics': {}, 'visitors_instances': []}

    def _parse_code(self, file_content, file_path):
        try:
            return ast.parse(file_content, type_comments=True)
        except SyntaxError:
            return None

    def _read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def export_to_csv(self, output_path, result):
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            is_new_file = not os.path.exists(output_path)
            with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=result.keys())
                if is_new_file:
                    writer.writeheader()
                writer.writerow(result)
        except PermissionError as pe:
            logger.error(f'Erro de permissão ao criar o arquivo: {pe}')
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            logger.error(f'Erro ao criar o arquivo: {e}')

    def export_matches_to_csv(self, output_path, matches):
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            is_new_file = not os.path.exists(output_path)
            with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['commit', 'file', 'lineno', 'code']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if is_new_file:
                    writer.writeheader()
                for match in matches:
                    writer.writerow(match)
        except Exception as e:
            logger.error(f'Erro ao criar o arquivo de matches: {e}')
