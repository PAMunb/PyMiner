import ast

class LiteralStringInterpolationVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'fstring' : 0,
            'fstring_files' : set(),
         }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def visit_JoinedStr(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # print(f'Encontrado: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['fstring'] += 1
            if self.current_file not in self.metrics['fstring_files']:
                self.metrics['fstring_files'].add(self.current_file)
        self.generic_visit(node)
