import ast

class UnpackVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'assign_unpack': 0,
            'list_unpack': 0,
            'tuple_unpack': 0,
            'set_unpack': 0,
            'dict_unpack': 0,
            'call_kwargs_unpack': 0,
            'call_args_unpack': 0,
            'assign_unpack_files': set(),
            'list_unpack_files': set(),
            'tuple_unpack_files': set(),
            'set_unpack_files': set(),
            'dict_unpack_files': set(),
            'call_kwargs_unpack_files': set(),
            'call_args_unpack_files': set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual
        

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_Assign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Detecta o uso de *rest em atribuições para PEP 3132
            # print(f'Encontrado: {ast.dump(node, annotate_fields=True, indent=1)}')
            for target in node.targets:
                # Verifica se o target é uma Tuple ou List que contém um Starred
                if isinstance(target, (ast.Tuple, ast.List)) and any(isinstance(elt, ast.Starred) for elt in target.elts):
                    self.metrics['assign_unpack'] += 1
                    if self.current_file not in self.metrics['assign_unpack_files']:
                        self.metrics['assign_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_List(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Ignora listas em atribuições, pois serão contadas por visit_Assign
            if not isinstance(node.ctx, ast.Store) and any(isinstance(elt, ast.Starred) for elt in node.elts):
                self.metrics['list_unpack'] += 1
                if self.current_file not in self.metrics['list_unpack_files']:
                    self.metrics['list_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Tuple(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Ignora tuplas em atribuições, pois serão contadas por visit_Assign
            if not isinstance(node.ctx, ast.Store) and any(isinstance(elt, ast.Starred) for elt in node.elts):
                self.metrics['tuple_unpack'] += 1
                if self.current_file not in self.metrics['tuple_unpack_files']:
                    self.metrics['tuple_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Set(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Detecta desempacotamento em sets (PEP 448)
            if any(isinstance(elt, ast.Starred) for elt in node.elts):
                self.metrics['set_unpack'] += 1
                if self.current_file not in self.metrics['set_unpack_files']:
                    self.metrics['set_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Dict(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Detecta desempacotamento em dicionários (PEP 448)
            if any(key is None for key in node.keys):  # None indica **dict
                self.metrics['dict_unpack'] += 1
                if self.current_file not in self.metrics['dict_unpack_files']:
                    self.metrics['dict_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Call(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Detecta desempacotamento em chamadas de função (PEP 448)
            if any(keyword.arg is None for keyword in node.keywords):  # None indica **kwargs
                self.metrics['call_kwargs_unpack'] += 1
                if self.current_file not in self.metrics['call_kwargs_unpack_files']:
                    self.metrics['call_kwargs_unpack_files'].add(self.current_file)
            if any(isinstance(arg, ast.Starred) for arg in node.args):  # *args
                self.metrics['call_args_unpack'] += 1
                if self.current_file not in self.metrics['call_args_unpack_files']:
                    self.metrics['call_args_unpack_files'].add(self.current_file)
        self.generic_visit(node)