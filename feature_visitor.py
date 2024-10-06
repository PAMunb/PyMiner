import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_union = 0
        self.feature_update = 0
        self.feature_all_stmts = 0
        self.dict_context = {}

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)

    # Verifica se uma exp Name é Dict e armazena em contexto
    def visit_Assign(self, node):
        # Captura atribuições de dicionários
        for target in node.targets:
            if isinstance(target, ast.Name):
                if isinstance(node.value, ast.Dict):  # Verifica se o valor atribuído é um dicionário
                    # Adiciona a variável ao contexto
                    # print(f'Encontrado node Dict: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.dict_context[target.id] = node.value
        self.generic_visit(node)

    # Verifica se uma operação binária usa o operador |
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.BitOr):  # Operação de união (|)
            # Verifica se o lado esquerdo é uma variável e se ela está no contexto
            left_dict = None
            if isinstance(node.left, ast.Name) and node.left.id in self.dict_context:
                left_dict = self.dict_context[node.left.id]

            # Verifica se o lado direito é uma variável e se ela está no contexto
            right_dict = None
            if isinstance(node.right, ast.Name) and node.right.id in self.dict_context:
                right_dict = self.dict_context[node.right.id]

            if left_dict is not None and right_dict is not None:
                # print(f'Encontrado operação de união de dicionários: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.feature_union += 1

        self.generic_visit(node)
        
    def visit_AugAssign(self, node):
        # Verifica se a operação é uma atribuição de união (|)
        if isinstance(node.op, ast.BitOr):  # Operação de união (|=)
            if isinstance(node.target, ast.Name) and node.target.id in self.dict_context:
                # print(f'Encontrado operação de atribuição de união de dicionários: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.feature_update += 1