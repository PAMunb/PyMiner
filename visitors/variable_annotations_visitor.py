import ast
        
class VariableAnnotationsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'variable_annotation': 0,
            'variable_annotation_files': set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_AnnAssign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['variable_annotation'] += 1
            self.metrics['variable_annotation_files'].add(self.current_file)
        self.generic_visit(node)