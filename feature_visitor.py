import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_unpack = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
        
    def visit_Starred(self, node):
        # Incrementa o contador para cada uso do operador '*'
        print(f'Encontrado node Unpack: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_unpack += 1
        # Continua a visita aos filhos deste nó
        self.generic_visit(node)