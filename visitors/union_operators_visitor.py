import ast

class UnionOperatorsVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.metrics = {
            'dict_union' : 0,
            'dict_union_update' : 0,
            'dict_union_files' : set(),
            'dict_union_update_files' : set()
         }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual
        self.dict_context = {}

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def visit_Assign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Captura atribuições de dicionários
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if isinstance(node.value, ast.Dict):
                        # print(f'Encontrado node Dict: {ast.dump(node, annotate_fields=True, indent=1)}')
                        self.dict_context[target.id] = node.value
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if isinstance(node.op, ast.BitOr):  # Operação de união (|)
                
                left_dict = None
                if isinstance(node.left, ast.Name) and node.left.id in self.dict_context:
                    left_dict = self.dict_context[node.left.id]
 
                right_dict = None
                if isinstance(node.right, ast.Name) and node.right.id in self.dict_context:
                    right_dict = self.dict_context[node.right.id]

                if left_dict is not None and right_dict is not None:
                    # print(f'Encontrado operação de união de dicionários: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.metrics['dict_union'] += 1
                    if self.current_file not in self.metrics['dict_union_files']:
                        self.metrics['dict_union_files'].add(self.current_file)
        self.generic_visit(node)
        
    def visit_AugAssign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if isinstance(node.op, ast.BitOr):  # Operação de união (|=)
                if isinstance(node.target, ast.Name) and node.target.id in self.dict_context:
                    # print(f'Encontrado operação de atribuição de união de dicionários: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.metrics['dict_union_update'] += 1
                    if self.current_file not in self.metrics['dict_union_update_files']:
                        self.metrics['dict_union_update_files'].add(self.current_file)
        self.generic_visit(node)