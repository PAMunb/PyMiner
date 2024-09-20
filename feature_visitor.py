import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
       self.feature_f_string = 0

    def visit_JoinedStr(self, node):
        # Contabiliza f-strings, que são representadas como JoinedStr no AST
        self.feature_f_string += 1
        self.generic_visit(node)
