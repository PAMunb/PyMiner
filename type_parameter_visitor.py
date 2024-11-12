import ast

class TypeParameterVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = { 
        'type_vars_bounds' : 0,
        'type_vars_constraints' : 0,
        'type_param_spec' : 0,
        'type_var_tuple' : 0,
        'type_alias' : 0,
        'type_vars_bounds_files' : set(),
        'type_vars_constraints_files' : set(),
        'type_param_spec_files' : set(),
        'type_var_tuple_files' : set(),
        'type_alias_files' : set(),
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
      
    def visit_TypeVar(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
        if node.bound:
            if isinstance(node.bound, ast.Tuple):
                self.metrics['type_vars_constraints'] += 1
                if self.current_file not in self.metrics['type_vars_constraints_files']:
                    self.metrics['type_vars_constraints_files'].add(self.current_file) 
            else:
                self.metrics['type_vars_bounds'] += 1             
                if self.current_file not in self.metrics['type_vars_bounds_files']:
                    self.metrics['type_vars_bounds_files'].add(self.current_file)                  
        self.generic_visit(node)
        
    def visit_ParamSpec(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
        self.metrics['type_param_spec'] += 1
        if self.current_file not in self.metrics['type_param_spec_files']:
            self.metrics['type_param_spec_files'].add(self.current_file) 
        self.generic_visit(node)
    
    def visit_TypeVarTuple(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
        self.metrics['type_var_tuple'] += 1
        if self.current_file not in self.metrics['type_var_tuple_files']:
            self.metrics['type_var_tuple_files'].add(self.current_file)
        self.generic_visit(node)
        
    def visit_TypeAlias(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
        self.metrics['type_alias'] += 1
        if self.current_file not in self.metrics['type_alias_files']:
            self.metrics['type_alias_files'].add(self.current_file)
        self.generic_visit(node)