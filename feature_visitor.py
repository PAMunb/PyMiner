import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_exception_group_count = 0
        self.feature_except_star_count = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
        
    def visit_ExceptHandler(self, node):
        # Contar grupos de exceções
        if isinstance(node.type, ast.Tuple):
            self.feature_exception_group_count += 1
        # No except* específico, usamos o atributo special
        elif node.type is None:
            # Não é o except* específico, então nada a fazer aqui
            pass
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_ExceptStar(self, node):
        # Conta o número de except* encontrados
        self.feature_except_star_count += 1
        self.generic_visit(node)  # Continue visiting child nodes
        