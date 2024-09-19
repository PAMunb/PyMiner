import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_union = 0
        self.feature_update = 0

    # Verifica se uma operação binária usa o operador |
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.BitOr):  # Operação de união (|)
            if isinstance(node.left, ast.Dict) or isinstance(node.right, ast.Dict):
                self.feature_union += 1
        self.generic_visit(node)

    # Verifica se uma operação in-place usa o operador |=
    def visit_AugAssign(self, node):
        if isinstance(node.op, ast.BitOr):  # Operação de atualização (|=)
            if isinstance(node.target, ast.Dict):
                self.feature_update += 1
        self.generic_visit(node)