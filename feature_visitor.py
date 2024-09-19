import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
        self.feature_type_annotation = 0

    def visit_AnnAssign(self, node):
        # Contabiliza anotações de tipo
        self.feature_type_annotation += 1
        self.generic_visit(node)  # Continua a visitar os nós filhos

    def visit_FunctionDef(self, node):
        # Contabiliza anotações de tipo em parâmetros e retorno
        if node.returns:
            self.feature_type_annotation += 1
        for arg in node.args.args:
            if arg.annotation:
                self.feature_type_annotation += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Contabiliza anotações de tipo em atributos
        for body_item in node.body:
            if isinstance(body_item, ast.AnnAssign):
                self.feature_type_annotation += 1
        self.generic_visit(node)