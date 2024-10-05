import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_unpacking_generalizations = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)

    def visit_Starred(self, node):
        # print(f'Encontrado node Starred: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_unpacking_generalizations += 1
        self.generic_visit(node)
        
    def visit_Dict(self, node):
       # Iterar sobre as chaves e valores do dicionário
        for key, value in zip(node.keys, node.values):
            # Verificar se a chave é None, o que indica o desempacotamento de dicionário (**)
            if key is None:
                # O valor associado será o objeto a ser desempacotado
                # print(f"Encontrado desempacotamento de dicionário: **{ast.dump(value)}")
                self.feature_unpacking_generalizations += 1
        self.generic_visit(node)
        
    def visit_Call(self, node):
    # Verificar a lista de keywords da chamada de função
        for keyword in node.keywords:
            if keyword.arg is None:
                # Isso indica o uso de **kwargs
                # print(f"Encontrado desempacotamento de **kwargs: {ast.dump(keyword.value)}")
                self.feature_unpacking_generalizations += 1
        
        # Continuar a visita aos nós filhos
        self.generic_visit(node)