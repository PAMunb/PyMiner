import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_unpack = 0
        
    def visit_Starred(self, node):
        # Incrementa o contador para cada uso do operador '*'
        self.feature_unpack += 1
        # Continua a visita aos filhos deste nó
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Visita os argumentos da função, se necessário
        self.generic_visit(node.args)
        # Não visita o corpo da função para evitar contagem duplicada
        for default in node.args.defaults:
            self.visit(default)

    def visit_Assign(self, node):
        # Verifica se é uma atribuição múltipla com desempacotamento
        for target in node.targets:
            if isinstance(target, ast.Tuple) or isinstance(target, ast.List):
                for element in target.elts:
                    if isinstance(element, ast.Starred):
                        self.visit_Starred(element)
        # Continua a visita para outros casos
        self.generic_visit(node)