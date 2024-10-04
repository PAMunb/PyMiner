import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_k_args = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
    
    def visit_Starred(self, node):
        # print(f'Encontrado node Starred: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_k_args += 1
        self.generic_visit(node)