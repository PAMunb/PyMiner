import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_annotation = 0
        self.feature_match = 0
        self.feature_case = 0
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
        
    def visit_Match(self, node):
        # Contar o match encontrado
        if isinstance(node, ast.Match):
            self.feature_match += 1
            print(f'Encontrado Match: {ast.dump(node, annotate_fields=True)}')
        self.generic_visit(node)  # Visita todos os filhos do nó

    def visit_Case(self, node):
        # Contar o case encontrado
        if isinstance(node, ast.Case):
            self.feature_case += 1
            print(f'Encontrado Case: {ast.dump(node, annotate_fields=True)}')
        self.generic_visit(node)  # Visita todos os filhos do nó
        