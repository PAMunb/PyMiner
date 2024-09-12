import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_k_args = 0
        

    def visit_FunctionDef(self, node):
        # Conta os parâmetros apenas nomeados na função
        keyword_only_params = node.args.kwonlyargs
        self.feature_k_args += len(keyword_only_params)
        # Continue visitando outros nós
        self.generic_visit(node)

    def visit_Arguments(self, node):
        # Conta os parâmetros apenas nomeados após o *
        if node.kwonlyargs:
            self.feature_k_args += len(node.kwonlyargs)
        # Continue visitando outros nós
        self.generic_visit(node)