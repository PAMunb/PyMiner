import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_nonlocal = 0
        

    def visit_Nonlocal(self, node):
        self.feature_nonlocal+= 1
        self.generic_visit(node)