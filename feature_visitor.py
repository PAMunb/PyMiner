import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_async_defs = 0
        self.feature_await_expressions = 0
        self.feature_awaitable_objects = 0
    
    def visit_FunctionDef(self, node):
        # Verifica se a função é uma corrotina
        if isinstance(node, ast.FunctionDef) and any(isinstance(decorator, ast.Name) and decorator.id == 'async' for decorator in node.decorator_list):
            self.feature_async_defs += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        # Conta funções definidas com async def
        self.feature_async_defs += 1
        self.generic_visit(node)

    def visit_Await(self, node):
        # Conta expressões que utilizam await
        self.feature_await_expressions += 1
        # Verifica se o await está usando um objeto awaitable
        if isinstance(node.value, ast.Call):
            self.feature_awaitable_objects += 1
        self.generic_visit(node)
        
    

      