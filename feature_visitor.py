import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_kw_defaults = 0
        self.feature_kw_args = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
        
    def visit_arguments(self, node):
        if node.kw_defaults:
            # print(f"Encontrado nodes Keyword-Only Arguments: **{ast.dump(node)}")
            self.feature_kw_defaults += len(node.kw_defaults)
        if node.kwonlyargs:
        # Adicionar o número de argumentos keyword-only (com ou sem valores padrão)
            # print(f"Encontrado nodes Keyword-Only Arguments: **{ast.dump(node)}")
            self.feature_kw_args += len(node.kwonlyargs)
        self.generic_visit(node)
        