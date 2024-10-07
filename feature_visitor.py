import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self, source_code):        
        self.feature_num_literals = 0
        self.source_code = source_code.splitlines()
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
        
    
    def visit_Constant(self, node):
        # Verifica se o node é um número
        # print(f'Encontrado Constante: {ast.dump(node, annotate_fields=True, indent=1)}')
        if isinstance(node.value, (int, float)):
            # Extrai a linha do código-fonte e verifica se há '_'
            literal_source = self.source_code[node.lineno - 1][node.col_offset:node.end_col_offset]
            if '_' in literal_source:
                # print(f'Encontrado Underscore: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.feature_num_literals += 1
        self.generic_visit(node)