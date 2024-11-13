import ast

class MatrixMultiplicationVisitor(ast.NodeVisitor):        
    def __init__(self):
        self.metrics = {
            'matrix_multiplication' : 0,
            'matrix_multiplication_files' : set(),
         }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
    
    def visit_BinOp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Verifica se o operador é o novo operador de multiplicação de matrizes `@`
            if isinstance(node.op, ast.MatMult):
                self.metrics['matrix_multiplication'] += 1
                if self.current_file not in self.metrics['matrix_multiplication_files']:
                    self.metrics['matrix_multiplication_files'].add(self.current_file)
        self.generic_visit(node)
        
    

      