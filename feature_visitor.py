import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self): 
        self.feature_type_vars_bounds = 0
        self.feature_type_vars_constraints = 0
        self.feature_type_param_spec = 0
        self.feature_type_var_tuple = 0
        self.feature_type_alias = 0
        self.feature_all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            #print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.feature_all_stmts += 1
        super().generic_visit(node)
      
    def visit_TypeVar(self, node):
        if node.bound:
            if isinstance(node.bound, ast.Tuple):
                # print(f'Encontrado node TypeVar.constraints: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.feature_type_vars_constraints += 1 
            else:
                # print(f'Encontrado node TypeVar.bound: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.feature_type_vars_bounds += 1              
        self.generic_visit(node)
        
    def visit_ParamSpec(self, node):
        # print(f'Encontrado node ParamSpec: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_type_param_spec += 1
        self.generic_visit(node)
    
    def visit_TypeVarTuple(self, node):
        # print(f'Encontrado node TypeVarTuple: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_type_var_tuple += 1
        self.generic_visit(node)
        
    def visit_TypeAlias(self, node):
        # print(f'Encontrado node TypeAlias: {ast.dump(node, annotate_fields=True, indent=1)}')
        self.feature_type_alias += 1
        self.generic_visit(node)