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
            if not isinstance(decorator, ast.Name) and not isinstance(decorator, ast.Attribute):
                if isinstance(decorator, ast.Call) and not self.is_simple_call(decorator):
                    # Conta decoradores complexos
                    # print(f'Encontrado no IF1: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                    self.metrics['decorator_with_expressions'] += 1
                    if self.current_file not in self.metrics['decorator_with_expressions_files']:
                        self.metrics['decorator_with_expressions_files'].add(self.current_file)
                    self.generic_visit(decorator)
                if isinstance(decorator, (ast.BinOp, ast.UnaryOp, ast.IfExp, ast.Lambda, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp,  ast.Compare, ast.Try, ast.ExceptHandler)):
                    # print(f'Encontrado no IF2: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                    self.metrics['decorator_with_expressions'] += 1
                    if self.current_file not in self.metrics['decorator_with_expressions_files']:
                        self.metrics['decorator_with_expressions_files'].add(self.current_file)
                    self.generic_visit(decorator)
                    
                    
    def is_simple_call(self, node):
        """
        Verifica se um decorador ast.Call é simples (PEP 318).
        Retorna True para simples, False para complexo (PEP 614).
        """
        if not isinstance(node, ast.Call):
            return False

        if not isinstance(node.func, (ast.Name, ast.Attribute)):
            return False

        # Verifica se existe qualquer expressão complexa nos argumentos
        if any(not isinstance(arg, (ast.Constant, ast.Name)) and isinstance(arg, (ast.BinOp, ast.UnaryOp, ast.IfExp, ast.Lambda,
                ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
                ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp,  ast.Compare, ast.Try, ast.ExceptHandler)) for arg in node.args):
            return False

        # Verifica se existe qualquer expressão complexa nas palavras-chave
        if any(not isinstance(keyword.value, (ast.Constant, ast.Name)) and isinstance(keyword.value, (ast.BinOp, ast.UnaryOp, ast.IfExp, ast.Lambda,
                ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
                ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp, ast.Compare, ast.Try, ast.ExceptHandler)) for keyword in node.keywords):
            return False

        return True
