import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):        
                self.feature_annotation_count = 0
    
    def visit_AnnAssign(self, node):
        """Conta declarações com anotações de tipo."""
        self.feature_annotation_count += 1
        self.generic_visit(node)  # Continue visitando os subnós
        
    """O CODIGO ABAIXO É BEM REFINADO MAS AO UTILIZA-LO ELE DUPLICA OS RESULTADOS

    def visit_FunctionDef(self, node):
        Visita funções para contar variáveis anotadas dentro delas.
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign):
                self.feature_annotation_count += 1
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        Visita classes para contar atributos de classe anotados.
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign):
                self.feature_annotation_count += 1
        self.generic_visit(node)"""