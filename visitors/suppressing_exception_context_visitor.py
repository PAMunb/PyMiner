import ast

class SuppressingExceptionContextVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'suppressing_exception_context': 0,
            'suppressing_exception_context_files': set(),
            'statements': 0
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def generic_visit(self, node):
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['statements'] += 1
        super().generic_visit(node)
        
    def visit_Raise(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.cause is not None and isinstance(node.cause, ast.Constant) and node.cause.value is None:
                self.metrics['suppressing_exception_context'] += 1
                if self.current_file not in self.metrics['suppressing_exception_context_files']:
                    self.metrics['suppressing_exception_context_files'].add(self.current_file)
        self.generic_visit(node)