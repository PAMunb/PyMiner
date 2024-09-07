import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.feature_annotation = 0
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
      
    def visit_AsyncFunctionDef(self, node):
        # print(f'Encontrado node AsyncFunctionDef: {ast.dump(node, annotate_fields=True, indent=4)}')             
        for arg in node.args.args:
            if arg.annotation:
                # print(f'Encontrado node Arg: {ast.dump(arg, annotate_fields=True, indent=4)}')
                self.feature_annotation += 1        
        if node.returns:
                self.feature_annotation += 1     
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # print(f'Encontrado node FunctionDef: {ast.dump(node, annotate_fields=True, indent=4)}')             
        for arg in node.args.args:
            if arg.annotation:
                # print(f'Encontrado node Arg: {ast.dump(arg, annotate_fields=True, indent=4)}')
                self.feature_annotation += 1
        if node.returns:
                self.feature_annotation += 1     
        self.generic_visit(node)