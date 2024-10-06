import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_args_return_annotation = 0
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
      
    def visit_arg(self, node):
        if node.annotation:
            # print(f'Encontrado node Arg: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.function_args_return_annotation += 1  
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):           
        if node.returns:
                # print(f'Encontrado node AsyncFunctionDef: {ast.dump(node, annotate_fields=True, indent=1)}')  
                self.function_args_return_annotation += 1     
        self.generic_visit(node)

    def visit_FunctionDef(self, node):         
        if node.returns:
                # print(f'Encontrado node FunctionDef: {ast.dump(node, annotate_fields=True, indent=1)}')    
                self.function_args_return_annotation += 1     
        self.generic_visit(node)