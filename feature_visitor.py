import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):      
        self.async_for = 0             # Contador para 'async for'
        self.async_with = 0            # Contador para 'async with'
        self.async_list_comprehensions = 0   # Contador para compreensões de lista
        self.async_set_comprehensions = 0    # Contador para compreensões de conjunto
        self.async_dict_comprehensions = 0   # Contador para compreensões de dicionário
        self.async_generator_expressions = 0  # Contador para expressões geradoras
        self.feature_all_stmts = 0     # Contador total de declarações

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)

    def visit_AsyncFor(self, node):
        # print(f'Encontrado node Async For: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.async_for += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        # print(f'Encontrado node Async With: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.async_with += 1
        self.generic_visit(node)

    def visit_ListComp(self, node):
        if node.generators:
            for gener in node.generators:
                if gener.is_async == True:
                    # print(f'Encontrado node List Comprehension: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.async_list_comprehensions += 1
                    break
        self.generic_visit(node)

    def visit_SetComp(self, node):
        if node.generators:
            for gener in node.generators:
                if gener.is_async == True:
                    # print(f'Encontrado node Set Comprehension: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.async_set_comprehensions += 1
                    break
        self.generic_visit(node)

    def visit_DictComp(self, node):
        if node.generators:
            for gener in node.generators:
                if gener.is_async == True:
                    # print(f'Encontrado node Dict Comprehension: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.async_dict_comprehensions += 1
                    break
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        if node.generators:
            for gener in node.generators:
                if gener.is_async == True:
                    # print(f'Encontrado node Generator Expression: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.async_generator_expressions += 1
                    break
        self.generic_visit(node)