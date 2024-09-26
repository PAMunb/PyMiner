import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_async_generators = 0  # Contador para geradores assíncronos
         # Contador para laços async for

    def visit_AsyncFunctionDef(self, node):
        # Verifica se a função assíncrona contém o "yield", ou seja, é um gerador assíncrono
        if any(isinstance(n, ast.Yield) for n in ast.walk(node)):
            self.feature_async_generators += 1
        
        # Continua a visita para outros nós
        self.generic_visit(node)
