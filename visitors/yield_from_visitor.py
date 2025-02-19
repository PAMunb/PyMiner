import ast

class YieldFromVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'yield_from': 0,
            'yield_from_files': set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_YieldFrom(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['yield_from'] += 1
            self.metrics['yield_from_files'].add(self.current_file)
        self.generic_visit(node)