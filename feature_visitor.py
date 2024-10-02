import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self, source_code):        
        self.feature_num_literals = 0
        self.source_code = source_code.splitlines()
    
    def visit_Constant(self, node):
        # Verifica se o node é um número
        if isinstance(node.value, (int, float)):
            # Extrai a linha do código-fonte e verifica se há '_'
            literal_source = self.source_code[node.lineno - 1][node.col_offset:node.end_col_offset]
            if '_' in literal_source:
                self.feature_num_literals += 1
        self.generic_visit(node)

    def visit_Num(self, node):
        # Para compatibilidade com versões anteriores do Python (antes do 3.8)
        if isinstance(node.n, (int, float)):
            literal_source = self.source_code[node.lineno - 1][node.col_offset:node.end_col_offset]
            if '_' in literal_source:
                self.feature_num_literals += 1
        self.generic_visit(node)

