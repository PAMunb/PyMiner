import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_count = 0
        self.feature_while = 0
        
    # def visit_While(self, node):
    #     if isinstance(node, ast.While):
    #         self.feature_while += 1
    #         # print(f'Encontrado node While: {ast.dump(sub_node, annotate_fields=True, indent=4)}')
    #     self.generic_visit(node)

    def visit(self, node):
        if isinstance(node, ast.While):
            self.feature_while += 1
        if isinstance(node, ast.stmt):
            self.feature_count += 1
            # print(f'Encontrado node Statement: {ast.dump(node, annotate_fields=True, indent=4)}')
        self.generic_visit(node)