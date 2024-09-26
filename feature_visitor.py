import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):      
        self.feature_async_comprehension_count = 0
        self.feature_async_for_count = 0
        self.feature_async_function_count = 0

    def visit_AsyncComprehension(self, node):
        """Conta compreensões assíncronas."""
        self.feature_async_comprehension_count += 1
        self.generic_visit(node)

    #parte refinada
    def visit_AsyncFor(self, node):
        """Conta loops assíncronos."""
        self.feature_async_for_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Conta definições de funções assíncronas."""
        self.feature_async_function_count += 1
        self.generic_visit(node)