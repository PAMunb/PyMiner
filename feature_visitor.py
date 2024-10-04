import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_fstring = 0               # Contador de f-strings
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)

    def visit_JoinedStr(self, node):
        # print(f'Encontrado node JoinedStr: {ast.dump(node, annotate_fields=True, indent=1)}')
        """Visita uma f-string ('JoinedStr' representa uma f-string no AST)."""
        self.feature_fstring += 1
        self.generic_visit(node)