import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_async_defs = 0
        self.feature_await_expressions = 0
        self.feature_awaitable_objects = 0
        self.feature_async_fors = 0
        self.feature_async_withs = 0
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        # Conta funções definidas com async def
        self.feature_async_defs += 1
        self.generic_visit(node)

    def visit_Await(self, node):
        # Conta expressões que utilizam await
        self.feature_await_expressions += 1
        
        # Verifica se o valor de await é um objeto que pode ser aguardado
        if isinstance(node.value, (ast.Call, ast.GeneratorExp, ast.YieldFrom)):
            self.feature_awaitable_objects += 1
        
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        # Conta loops assíncronos com async for
        self.feature_async_fors += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        # Conta blocos de contexto assíncronos com async with
        self.feature_async_withs += 1
        self.generic_visit(node)
        
    

      