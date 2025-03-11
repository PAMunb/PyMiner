import logging
import csv
import sys
from datetime import datetime
import os
import warnings

from feature_counter import FeatureCounter
from visitors.assignment_expression_visitor import AssignmentExpressionVisitor
from visitors.suppressing_exception_context_visitor import SuppressingExceptionContextVisitor
from visitors.type_parameter_visitor import TypeParameterVisitor
from visitors.keyword_only_arguments_visitor import KeywordOnlyArgumentsVisitor
from visitors.function_annotations_visitor import FunctionAnnotationsVisitor
from visitors.nonlocal_statement_visitor import NonlocalStatementVisitor
from visitors.unpack_visitor import UnpackVisitor
from visitors.structural_pattern_matching_visitor import StructuralPatternMatchingVisitor
from visitors.exception_groups_visitor import ExceptionGroupsVisitor
from visitors.literal_string_interpolation_visitor import LiteralStringInterpolationVisitor
from visitors.coroutines_visitor import CoroutinesVisitor
from visitors.matrix_multiplication_visitor import MatrixMultiplicationVisitor
from visitors.asynchronous_comprehension_visitor import AsynchronousComprehensionVisitor
from visitors.variable_annotations_visitor import VariableAnnotationsVisitor
from visitors.yield_from_visitor import YieldFromVisitor

# Desabilitar todos os SyntaxWarnings para evitar que apareçam durante a execução
warnings.filterwarnings("ignore", category=SyntaxWarning)

logger = logging.getLogger(__name__)

def process_repository(repo_info, start_date, end_date, steps):
    
    owner = repo_info["owner"]
    repo = repo_info["repo"]
    
    logger.info(f"Iniciando o processamento do repositório {owner}/{repo}")

    repo_url = f"https://github.com/{owner}/{repo}.git"
    
    feature_counter = FeatureCounter(
        repo_url,
        [AsynchronousComprehensionVisitor, MatrixMultiplicationVisitor, CoroutinesVisitor,
         LiteralStringInterpolationVisitor, ExceptionGroupsVisitor, StructuralPatternMatchingVisitor, UnpackVisitor,
         NonlocalStatementVisitor, FunctionAnnotationsVisitor, KeywordOnlyArgumentsVisitor, TypeParameterVisitor, YieldFromVisitor, AssignmentExpressionVisitor,
         VariableAnnotationsVisitor,SuppressingExceptionContextVisitor],
        start_date, end_date, steps
    )

    feature_counter.process()
    logger.info(f"Processamento do repositório {owner}/{repo} concluído e resultados salvos.")


if __name__ == "__main__":

    # Verifica se o caminho do arquivo CSV foi fornecido como argumento de linha de comando
    # executar o comando: python3 main.py python-projects.csv
    if len(sys.argv) < 2:
        logger.error("Por favor, forneça o caminho para o arquivo CSV como argumento de linha de comando.")
        sys.exit(1)
    
    # Caminho para o arquivo CSV
    csv_file_path = sys.argv[1]
    
    # Configurações para o processamento
    start_date = datetime(2008, 1, 1)  # Data inicio para filtrar os commits
    end_date = datetime(2024, 12, 31)  # Data final para filtrar os commits
    steps = 30  # Número de dias entre os commits
    
    # Lista de repositórios para processar
    repositories = []

    # Lê os dados do arquivo CSV e adiciona os repositórios à lista
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            repository_info = {"owner": row["name"].split('/')[0], "repo": row["name"].split('/')[1]}
            file_path = f"results/{repository_info['owner']}_{repository_info['repo']}.csv"  # Caminho para o arquivo CSV do repositório, exemplo: "results/owner"]}_{repo}.csv"
            if os.path.isfile(file_path):
                logger.info(f"Repositório {repository_info['owner']}/{repository_info['repo']} já processado, pulando repositório.")
                continue
            repositories.append(repository_info)

    # Processa cada repositório sequencialmente
    for repo_info in repositories:
        try:
            process_repository(repo_info, start_date, end_date, steps)
        except Exception as e:
            logger.error(f"Erro ao processar o repositório {repo_info['owner']}/{repo_info['repo']}: {str(e)}")
