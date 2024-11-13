import ast

class KeywordOnlyArgumentsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'kw_defaults' : 0,
            'kw_args' : 0,
            'kw_defaults_files' : set(),
            'kw_args_files' : set()
         }     
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_arguments(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.kw_defaults:
                # print(f"Encontrado nodes Keyword-Only Arguments: **{ast.dump(node)}")
                self.metrics['kw_defaults'] += len(node.kw_defaults) # Adicionar o número de argumentos keyword-only (com ou sem valores padrão)feature_kw_defaults += len(node.kw_defaults)
                if self.current_file not in self.metrics['kw_defaults_files']:
                    self.metrics['kw_defaults_files'].add(self.current_file)
            if node.kwonlyargs:
                self.metrics['kw_args'] += len(node.kwonlyargs) # feature_kw_args += len(node.kwonlyargs)
                if self.current_file not in self.metrics['kw_args_files']:
                    self.metrics['kw_args_files'].add(self.current_file)
        self.generic_visit(node)
        