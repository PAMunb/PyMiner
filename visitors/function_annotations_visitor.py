import ast

class FunctionAnnotationsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'function_args_annotation' : 0,
            'function_return_annotation' : 0,
            'function_args_annotation_files' : set(),
            'function_return_annotation_files' : set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual
        
    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
    def visit_arg(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.annotation:
                # print(f'Encontrado node Arg: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.metrics['function_args_annotation'] += 1
                if self.current_file not in self.metrics['function_args_annotation_files']:
                    self.metrics['function_args_annotation_files'].add(self.current_file)  
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)                   
            if node.returns:
                    # print(f'Encontrado node AsyncFunctionDef: {ast.dump(node, annotate_fields=True, indent=1)}')  
                    self.metrics['function_return_annotation'] += 1
                    if self.current_file not in self.metrics['function_return_annotation_files']:
                        self.metrics['function_return_annotation_files'].add(self.current_file)   
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)         
            if node.returns:
                    # print(f'Encontrado node FunctionDef: {ast.dump(node, annotate_fields=True, indent=1)}')    
                    self.metrics['function_return_annotation'] += 1
                    if self.current_file not in self.metrics['function_return_annotation_files']:
                        self.metrics['function_return_annotation_files'].add(self.current_file)   
        self.generic_visit(node)