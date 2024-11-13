import ast

class AsynchronousComprehensionVisitor(ast.NodeVisitor):
    def __init__(self):      
        self.metrics = {
            'async_list_comprehensions' : 0,   # Contador para compreensões de lista
            'async_set_comprehensions' : 0,    # Contador para compreensões de conjunto
            'async_dict_comprehensions' : 0,   # Contador para compreensões de dicionário
            'async_generator_expressions' : 0,  # Contador para expressões geradoras
            'async_list_comprehensions_files': set(), 
            'async_set_comprehensions_files': set(),   
            'async_dict_comprehensions_files': set(),  
            'async_generator_expressions_files': set()
         }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def visit_ListComp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if any(gen.is_async for gen in node.generators):
                self.metrics['async_list_comprehensions'] += 1
                if self.current_file not in self.metrics['async_list_comprehensions_files']:
                    self.metrics['async_list_comprehensions_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if any(gen.is_async for gen in node.generators):
                self.metrics['async_set_comprehensions'] += 1
                if self.current_file not in self.metrics['async_set_comprehensions_files']:
                    self.metrics['async_set_comprehensions_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if any(gen.is_async for gen in node.generators):
                self.metrics['async_dict_comprehensions'] += 1
                if self.current_file not in self.metrics['async_dict_comprehensions_files']:
                    self.metrics['async_dict_comprehensions_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if any(gen.is_async for gen in node.generators):
                self.metrics['async_generator_expressions'] += 1
                if self.current_file not in self.metrics['async_generator_expressions_files']:
                    self.metrics['async_generator_expressions_files'].add(self.current_file)
        self.generic_visit(node)