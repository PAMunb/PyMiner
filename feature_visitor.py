import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self): 
          
        self.feature_type_vars = 0
        self.feature_type_params_in_classes = 0
        self.feature_type_params_in_functions = 0
      
    def visit_TypeVar(self, node):
        self.feature_type_vars += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Verifica se a classe tem parâmetros de tipo
        if hasattr(node, 'type_params') and node.type_params:
            self.feature_type_params_in_classes += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Verifica se a função tem parâmetros de tipo
        if hasattr(node, 'type_params') and node.type_params:
            self.feature_type_params_in_functions += 1
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # Verifica se a anotação é do tipo TypeAlias
        if isinstance(node.target, ast.Name) and isinstance(node.annotation, ast.Subscript):
            self.feature_type_vars += 1
        self.generic_visit(node)