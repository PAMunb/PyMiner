import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_matrix_mult = 0
    
    def visit_BinOp(self, node):
        # Verifica se o operador é o novo operador de multiplicação de matrizes `@`
        if isinstance(node.op, ast.MatMult):
            self.feature_matrix_mult += 1
        # Continua visitando os filhos do nó
        self.generic_visit(node)
        
    

      