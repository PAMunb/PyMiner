import ast

class NonlocalStatementVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'nonlocal' : 0,
            'nonlocal_files' : set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def visit_Nonlocal(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['nonlocal'] += 1
            if self.current_file not in self.metrics['nonlocal_files']:
                self.metrics['nonlocal_files'].add(self.current_file)
        self.generic_visit(node)