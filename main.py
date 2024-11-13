import logging
import csv
import sys
from datetime import datetime

from feature_counter import FeatureCounter
from visitors.type_hint_visitor import TypeHintVisitor
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
from visitors.underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor
from visitors.asynchronous_comprehension_visitor import AsynchronousComprehensionVisitor
from visitors.union_operators_visitor import UnionOperatorsVisitor
from visitors.decorator_with_expressions_visitor import DecoratorsWithExpressionVisitor

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    # Verifica se o caminho do arquivo CSV foi fornecido como argumento de linha de comando
    # executar o comando: python3 main.py python-projects.csv
    if len(sys.argv) < 2:
        logger.error("Por favor, forneça o caminho para o arquivo CSV como argumento de linha de comando.")
        sys.exit(1)
    
    # Caminho para o arquivo CSV
    csv_file_path = sys.argv[1]
    
    # Exemplo de data e número de threads
    start_date = datetime(2012, 1, 1)  # Data para filtrar os commits
    max_threads = 4  # Número de threads a ser utilizado
    steps = 30 # Número de dias entre os commits
    
    # Lista de repositórios para processar
    repositories = []

    # Lê os dados do arquivo CSV e adiciona os repositórios à lista
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            repository_info = {"owner": row["name"].split('/')[0], "repo": row["name"].split('/')[1]}
            repositories.append(repository_info)

    # Processa cada repositório
    for repo_info in repositories:
        owner = repo_info["owner"]
        repo = repo_info["repo"]
        repo_url = f"https://github.com/{owner}/{repo}.git"
        feature_counter = FeatureCounter(repo_url, [DecoratorsWithExpressionVisitor,UnionOperatorsVisitor,AsynchronousComprehensionVisitor,UnderscoresNumericLiteralsVisitor,MatrixMultiplicationVisitor,CoroutinesVisitor,LiteralStringInterpolationVisitor,ExceptionGroupsVisitor,StructuralPatternMatchingVisitor,UnpackVisitor,NonlocalStatementVisitor,FunctionAnnotationsVisitor,KeywordOnlyArgumentsVisitor,TypeParameterVisitor,TypeHintVisitor], start_date, max_threads, steps)
        feature_counter.process()
        feature_counter.export_to_csv(f"results/{owner}_{repo}.csv")