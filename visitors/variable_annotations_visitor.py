import ast
        
class VariableAnnotationsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            # Métricas para AnnAssign (variável anotada)
            'variable_annotation': 0,
            'variable_annotation_files': set(),

            # Métricas para Assign (atribuição simples)
            'assign': 0,
            'assign_files': set(),
            
            # Métricas para Assign com type comment (x = 10  # type: int)
            'assign_with_type_comment': 0,
            'assign_with_type_comment_files': set(),

            # Métricas para AugAssign (atribuição aumentada: +=, -=, etc.)
            'aug_assign': 0,
            'aug_assign_files': set(),
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
        
    def visit_AnnAssign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # print(f'Encontrado node AnnAssign: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['variable_annotation'] += 1
            self.metrics['variable_annotation_files'].add(self.current_file)
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        """
        Captura atribuições simples (x = 10, x, y = 1, 2 etc.) e
        separa quando há um type_comment de quando não há.
        """
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)

            if getattr(node, 'type_comment', None):
                # Se 'node.type_comment' existir e for diferente de None, 
                # temos um type comment
                # print(f'Encontrado node AssignTypeComment: {ast.dump(node, annotate_fields=True, indent=1)}')
                self.metrics['assign_with_type_comment'] += 1
                self.metrics['assign_with_type_comment_files'].add(self.current_file)
            else:
                # print(f'Encontrado node Assign: {ast.dump(node, annotate_fields=True, indent=1)}')
                # Se não houver type_comment
                self.metrics['assign'] += 1
                self.metrics['assign_files'].add(self.current_file)

        self.generic_visit(node)

    def visit_AugAssign(self, node):
        """ Captura atribuições aumentadas (x += 1, x -= 2, etc.). """
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # print(f'Encontrado node AugAssign: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.metrics['aug_assign'] += 1
            self.metrics['aug_assign_files'].add(self.current_file)
        self.generic_visit(node)