import ast

class CoroutinesVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'async_def' : 0,
            'await_expressions' : 0,
            'async_for' : 0,
            'async_with' : 0,
            'async_def_files' : set(),
            'await_expressions_files' : set(),
            'async_for_files' : set(),
            'async_with_files' : set()
        }

        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_AsyncFunctionDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Conta funções definidas com async def
            self.metrics['async_def'] += 1
            if self.current_file not in self.metrics['async_def_files']:
                self.metrics['async_def_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Await(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Conta expressões que utilizam await
            self.metrics['await_expressions'] += 1
            if self.current_file not in self.metrics['await_expressions_files']:
                self.metrics['await_expressions_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Conta loops assíncronos com async for
            self.metrics['async_for'] += 1
            if self.current_file not in self.metrics['async_for_files']:
                self.metrics['async_for_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Conta blocos de contexto assíncronos com async with
            self.metrics['async_with'] += 1
            if self.current_file not in self.metrics['async_with_files']:
                self.metrics['async_with_files'].add(self.current_file)
        self.generic_visit(node)
        
    

      