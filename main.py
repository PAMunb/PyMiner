import logging

from feature_counter import FeatureCounter
from type_hint_visitor import TypeHintVisitor
from type_parameter_visitor import TypeParameterVisitor
from keyword_only_arguments_visitor import KeywordOnlyArgumentsVisitor
from function_annotations_visitor import FunctionAnnotationsVisitor
from nonlocal_statement_visitor import NonlocalStatementVisitor
from unpack_visitor import UnpackVisitor
from structural_pattern_matching_visitor import StructuralPatternMatchingVisitor
from exception_groups_visitor import ExceptionGroupsVisitor
from literal_string_interpolation_visitor import LiteralStringInterpolationVisitor
from coroutines_visitor import CoroutinesVisitor
from matrix_multiplication_visitor import MatrixMultiplicationVisitor
from underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor
from asynchronous_comprehension_visitor import AsynchronousComprehensionVisitor

import csv
import sys

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    # Verifica se o caminho do arquivo CSV foi fornecido como argumento de linha de comando
    if len(sys.argv) < 2:
        logger.error("Por favor, forneça o caminho para o arquivo CSV como argumento de linha de comando.")
        sys.exit(1)
    
    # Caminho para o arquivo CSV
    csv_file_path = sys.argv[1]
    
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
        feature_counter = FeatureCounter(repo_url, [AsynchronousComprehensionVisitor,UnderscoresNumericLiteralsVisitor,MatrixMultiplicationVisitor,CoroutinesVisitor,LiteralStringInterpolationVisitor,ExceptionGroupsVisitor,StructuralPatternMatchingVisitor,UnpackVisitor,NonlocalStatementVisitor,FunctionAnnotationsVisitor,KeywordOnlyArgumentsVisitor,TypeParameterVisitor,TypeHintVisitor])
        feature_counter.process()
        feature_counter.export_to_csv(f"results/{owner}_{repo}.csv")