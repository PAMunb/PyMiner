import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_fstring = 0               # Contador de f-strings
        self.comment_count = 0               # Contador de comentários dentro de f-strings
        self.feature_newline = 0               # Contador de quebras de linha dentro de f-strings
        self.feature_complex_expression = 0    # Contador de expressões complexas dentro de f-strings

    def visit_JoinedStr(self, node):
        """Visita uma f-string ('JoinedStr' representa uma f-string no AST)."""
        self.feature_fstring += 1
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                self.visit_FormattedValue(value)
    
    def visit_FormattedValue(self, node):
        """
        Conta comentários, quebras de linha e expressões complexas dentro das f-strings.
        """
        # Expressões complexas podem envolver subexpressões, operações matemáticas, etc.
        if isinstance(node.value, (ast.BinOp, ast.Call, ast.IfExp, ast.Compare)):
            self.feature_complex_expression += 1
        
        # Verifica o número de linhas em cada expressão (para encontrar quebras de linha)
        if hasattr(node.value, 'lineno') and hasattr(node.value, 'end_lineno'):
            if node.value.lineno != node.value.end_lineno:
                self.feature_newline += 1
        
        # Visita subnós para verificar comentários ou expressões complexas
        self.generic_visit(node)