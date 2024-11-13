import ast

class DecoratorsWithExpressionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'decorator_with_expressions' : 0,
            'decorator_with_expressions_files' : set(),
         }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    # Verifica cada função ou classe decorada
    def visit_FunctionDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self._count_decorators(node.decorator_list)
        self.generic_visit(node)

    # Função que identifica e conta decoradores simples ou complexos
    def _count_decorators(self, decorators):
        for decorator in decorators:
            if not isinstance(decorator, ast.Name):
                # Decorador complexo: expressão (ex: chamadas, acessos a atributos, etc.)
                self.metrics['decorator_with_expressions'] += 1
                if self.current_file not in self.metrics['decorator_with_expressions_files']:
                    self.metrics['decorator_with_expressions_files'].add(self.current_file)
                self.generic_visit(decorator)