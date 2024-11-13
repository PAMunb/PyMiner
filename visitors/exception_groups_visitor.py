import ast

class ExceptionGroupsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'except_star' : 0,
            'except_star_files' : set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name        
    def visit_TryStar(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.handlers:
                # print(f'Encontrado node exception*: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.metrics['except_star'] += 1
                if self.current_file not in self.metrics['except_star_files']:
                    self.metrics['except_star_files'].add(self.current_file)
        self.generic_visit(node)