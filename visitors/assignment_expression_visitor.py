import ast

class AssignmentExpressionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'assignment_expression': 0,
            'assignment_expression_files': set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_NamedExpr(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['assignment_expression'] += 1
            self.metrics['assignment_expression_files'].add(self.current_file)
        self.generic_visit(node)