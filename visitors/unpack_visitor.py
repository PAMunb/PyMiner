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
        if id(node) not in self.visited_nodes:
            self.visited_nodes.add(id(node))
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
        # Se já visitado, ignorar
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))
        # Se a lista contém um Starred, ela é um display de desempacotamento (PEP 448)
        # Mas somente se o contexto NÃO for de atribuição (Store)
        if not isinstance(node.ctx, ast.Store) and any(isinstance(elt, ast.Starred) for elt in node.elts):
            self.metrics['list_unpack'] += 1
            self.metrics['list_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Tuple(self, node):
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))
        # Se a tupla não está sendo usada como alvo de atribuição e contém Starred
        if not isinstance(node.ctx, ast.Store) and any(isinstance(elt, ast.Starred) for elt in node.elts):
            self.metrics['tuple_unpack'] += 1
            self.metrics['tuple_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Set(self, node):
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))
        # Verifica desempacotamento em sets (PEP 448)
        if any(isinstance(elt, ast.Starred) for elt in node.elts):
            self.metrics['set_unpack'] += 1
            self.metrics['set_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Dict(self, node):
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))
        # Em displays de dicionário, um desempacotamento é indicado por uma chave None (para **)
        if any(key is None for key in node.keys):
            self.metrics['dict_unpack'] += 1
            self.metrics['dict_unpack_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Call(self, node):
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))

        # Contadores para desempacotamento em chamadas (PEP 448)
        num_kwargs_unpack = 0
        num_args_unpack = 0

        # Para **kwargs: keyword.arg é None indica desempacotamento.
        for keyword in node.keywords:
            if keyword.arg is None:
                num_kwargs_unpack += 1

        # Para *args: identifica nós Starred em node.args.
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                num_args_unpack += 1

        # Só contabilizamos se houver MAIS de UM desempacotamento, pois um único desempacotamento
        # já era permitido antes da PEP 448.
        if num_kwargs_unpack > 1:
            # print(f'Encontrado múltiplos kwargs unpack: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['call_kwargs_unpack'] += 1
            self.metrics['call_kwargs_unpack_files'].add(self.current_file)

        if num_args_unpack > 1:
            # print(f'Encontrado múltiplos args unpack: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['call_args_unpack'] += 1
            self.metrics['call_args_unpack_files'].add(self.current_file)

        self.generic_visit(node)





