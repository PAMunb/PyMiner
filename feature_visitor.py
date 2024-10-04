import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_except_star_count = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
        
    def visit_TryStar(self, node):
        if node.handlers:
            # print(f'Encontrado node exception*: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_except_star_count += len(node.handlers)
        self.generic_visit(node)
        