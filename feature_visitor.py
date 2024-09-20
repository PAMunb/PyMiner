import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_num_literals = 0
    
    def visit_Constant(self, node):
        # No Python 3.8+ os literais numéricos são representados como ast.Constant
        if isinstance(node.value, (int, float)) and '_' in str(node.value):
            self.feature_num_literals += 1
        self.generic_visit(node)

    def visit_Num(self, node):
        # Em versões anteriores ao Python 3.8, os literais numéricos são ast.Num
        if isinstance(node.n, (int, float)) and '_' in str(node.n):
            self.feature_num_literals += 1
        self.generic_visit(node)