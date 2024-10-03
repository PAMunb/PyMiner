import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_except_star_count = 0
        self.feature_exception_group_count = 0

    def visit_ExceptStar(self, node):
        """Contar blocos except*."""
        self.feature_except_star_count += 1
        self.generic_visit(node)  # Visita nós filhos

    def visit_ExceptHandler(self, node):
        """Contar grupos de exceções normais."""
        if isinstance(node.type, ast.Tuple):
            self.feature_exception_group_count += 1
        self.generic_visit(node)  # Visita nós filhos
