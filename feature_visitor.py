import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_simple_decorators = 0
        self.feature_complex_decorators = 0

    # Verifica cada função ou classe decorada
    def visit_FunctionDef(self, node):
        self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    # Função que identifica e conta decoradores simples ou complexos
    def _count_decorators(self, decorators):
        for decorator in decorators:
            if isinstance(decorator, ast.Name):
                # Decorador simples: apenas um nome de função ou objeto
                self.feature_simple_decorators += 1
            else:
                # Decorador complexo: expressão (ex: chamadas, acessos a atributos, etc.)
                self.feature_complex_decorators += 1