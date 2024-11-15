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
                    
                    # print(f'Encontrado no IF1: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                    
                    self.metrics['decorator_with_expressions'] += 1
                    if self.current_file not in self.metrics['decorator_with_expressions_files']:
                        self.metrics['decorator_with_expressions_files'].add(self.current_file)
                    self.generic_visit(decorator)
                    
                elif isinstance(decorator, ast.Lambda):
                    if not self.is_simple_lambda(decorator):
                        
                        # print(f'Encontrado no IF2: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                        
                        self.metrics['decorator_with_expressions'] += 1
                        if self.current_file not in self.metrics['decorator_with_expressions_files']:
                            self.metrics['decorator_with_expressions_files'].add(self.current_file)
                        self.generic_visit(decorator)  
                        
                elif isinstance(decorator, (ast.BinOp, ast.UnaryOp)):
                    if not isinstance(decorator.left, ast.Constant) and not isinstance(decorator.right, ast.Constant):
                        
                        # print(f'Encontrado no IF3: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                        
                        self.metrics['decorator_with_expressions'] += 1
                        if self.current_file not in self.metrics['decorator_with_expressions_files']:
                            self.metrics['decorator_with_expressions_files'].add(self.current_file)
                        self.generic_visit(decorator)
                                                
                elif isinstance(decorator, (ast.IfExp, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp, ast.Try, ast.ExceptHandler)):
                    
                    # print(f'Encontrado no IF4: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                    
                    self.metrics['decorator_with_expressions'] += 1
                    if self.current_file not in self.metrics['decorator_with_expressions_files']:
                        self.metrics['decorator_with_expressions_files'].add(self.current_file)
                    self.generic_visit(decorator)
                elif isinstance(decorator, ast.Compare):
                    # Verifica se a comparação é entre dois objetos simples (como variáveis e constantes)
                    if not isinstance(decorator.left, (ast.Attribute, ast.Name, ast.Constant)) and not all(isinstance(comp, (ast.Attribute, ast.Name, ast.Constant)) for comp in decorator.comparators):
                        
                        # print(f'Encontrado no IF5: {ast.dump(decorator, annotate_fields=True, indent=1)}')
                        
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

        # Verifica se os argumentos são simples (constantes ou variáveis)
        for arg in node.args:
            if isinstance(arg, ast.Lambda):
                if not self.is_simple_lambda(arg):
                    return False
            if isinstance(arg, (ast.BinOp, ast.UnaryOp)):
                # Permite operações binárias simples com constantes
                if isinstance(arg.left, ast.Constant) and isinstance(arg.right, ast.Constant):
                    continue
                return False
            elif isinstance(arg, (ast.ListComp, ast.SetComp, ast.DictComp)):
                return False  # Exclui compreensões de listas como complexos
            elif isinstance(arg, (ast.IfExp, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set,
                                ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp,
                                ast.Try, ast.ExceptHandler)):
                return False  # Qualquer uma dessas expressões é considerada complexa
            # Adicionando verificação para comparações simples
            elif isinstance(arg, ast.Compare):
                # Verifica se a comparação é entre dois objetos simples (como variáveis e constantes)
                if isinstance(arg.left, (ast.Attribute, ast.Name, ast.Constant)) and all(isinstance(comp, (ast.Attribute, ast.Name, ast.Constant)) for comp in arg.comparators):
                    continue
                return False

        # Verifica se as palavras-chave têm expressões complexas
        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Lambda):
                if not self.is_simple_lambda(keyword.value):
                    return False
            if isinstance(keyword.value, (ast.BinOp, ast.UnaryOp)):
                # Permite operações binárias simples com constantes
                if isinstance(keyword.value.left, ast.Constant) and isinstance(keyword.value.right, ast.Constant):
                    continue
                return False
            elif isinstance(keyword.value, (ast.ListComp, ast.SetComp, ast.DictComp)):
                return False  # Exclui compreensões de listas como complexos
            elif isinstance(keyword.value, (ast.IfExp, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set,
                                            ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp,
                                            ast.Try, ast.ExceptHandler)):
                return False  # Qualquer uma dessas expressões é considerada complexa
            elif isinstance(keyword.value, ast.Compare):
                # Verifica se a comparação é entre dois objetos simples (como variáveis e constantes)
                if isinstance(keyword.value.left, (ast.Attribute, ast.Name, ast.Constant)) and all(isinstance(comp, (ast.Attribute, ast.Name, ast.Constant)) for comp in arg.comparators):
                    continue
                return False

        return True


    def is_simple_lambda(self, node):
        """
        Verifica se uma expressão lambda é simples ou complexa.
        Uma lambda é simples se sua expressão (node.body) for simples.
        """
        # Verifica se a expressão dentro da lambda é simples
        if isinstance(node.body, (ast.BinOp, ast.UnaryOp, ast.IfExp, ast.Lambda,
                                ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            return False  # Considera qualquer dessas expressões como complexa
        
        # Verifica se os argumentos são simples (constantes ou variáveis)
        for arg in node.args:
            if isinstance(arg, ast.Lambda):
                if not self.is_simple_lambda(arg):
                    return False
            if isinstance(arg, (ast.BinOp, ast.UnaryOp)):
                # Permite operações binárias simples com constantes
                if isinstance(arg.left, ast.Constant) and isinstance(arg.right, ast.Constant):
                    continue
                return False
            elif isinstance(arg, (ast.ListComp, ast.SetComp, ast.DictComp)):
                return False  # Exclui compreensões de listas como complexos
            elif isinstance(arg, (ast.IfExp, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set,
                                ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.BoolOp, 
                                ast.Try, ast.ExceptHandler)):
                return False  # Qualquer uma dessas expressões é considerada complexa
            elif isinstance(arg, ast.Compare):
                # Verifica se a comparação é entre dois objetos simples (como variáveis e constantes)
                if isinstance(arg.left, (ast.Attribute, ast.Name, ast.Constant)) and all(isinstance(comp, (ast.Attribute, ast.Name, ast.Constant)) for comp in arg.comparators):
                    continue
                return False

        return True  # Caso contrário, é simples