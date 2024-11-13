import ast

class UnderscoresNumericLiteralsVisitor(ast.NodeVisitor):

    def __init__(self):
        self.metrics = {
            'underscores_num_literals' : 0,
            'underscores_num_literals_files' : set(),
         }        
        self.source_code = ""
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def set_source_code(self, source_code):
        # Método para setar o código-fonte
        self.source_code = source_code.splitlines()
    
    def visit_Constant(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Verifica se o node é um número
            if isinstance(node.value, (int, float)):
                # Extrai a linha do código-fonte e verifica se há '_'
                literal_source = self.source_code[node.lineno - 1][node.col_offset:node.end_col_offset]
                if '_' in literal_source:
                    # print(f'Encontrado: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.metrics['underscores_num_literals'] += 1
                    if self.current_file not in self.metrics['underscores_num_literals_files']:
                        self.metrics['underscores_num_literals_files'].add(self.current_file)
        self.generic_visit(node)