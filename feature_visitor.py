import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_unpack_lists = 0
        self.feature_unpack_tuples = 0
        self.feature_unpack_dicts = 0
        self.feature_call_unpack_args = 0
        self.feature_call_unpack_kwargs = 0

    def visit_List(self, node):
        # Verifica se há desempacotamento usando *
        
        if any(isinstance(elt, ast.Starred) for elt in node.elts):
            print("list")
            self.feature_unpack_lists += 1
        self.generic_visit(node)

    def visit_Tuple(self, node):
        # Verifica se há desempacotamento usando *
        if any(isinstance(elt, ast.Starred) for elt in node.elts):
            self.feature_unpack_tuples += 1
        self.generic_visit(node)

    def visit_Dict(self, node):
        # Verifica se há desempacotamento usando **
        if any(isinstance(key, ast.Starred) for key in node.keys):
            self.feature_unpack_dicts += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        # Verifica se há desempacotamento usando *
        if any(isinstance(kwarg, ast.Starred) for kwarg in node.args):
            self.feature_call_unpack_args += 1
        # Verifica se há desempacotamento usando **
        if any(isinstance(kwarg, ast.keyword) and isinstance(kwarg.value, ast.Starred) for kwarg in node.keywords):
            self.feature_call_unpack_kwargs += 1
        self.generic_visit(node)