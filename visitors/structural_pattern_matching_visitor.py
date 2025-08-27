import ast

class StructuralPatternMatchingVisitor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.metrics = {
            'pattern_match' : 0,
            'pattern_as' : 0,
            'pattern_or' : 0,
            'pattern_sequence' : 0,
            'pattern_mapping' : 0,
            'pattern_class' : 0,
            'pattern_value' : 0,
            'pattern_singleton' : 0,
            'pattern_star' : 0,
            'pattern_match_files' : set(),
            'pattern_as_files' : set(),
            'pattern_or_files' : set(),
            'pattern_sequence_files' : set(),
            'pattern_mapping_files' : set(),
            'pattern_class_files' : set(),
            'pattern_value_files' : set(),
            'pattern_singleton_files' : set(),
            'pattern_star_files' : set()
        }

        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.current_file = ""  # Para armazenar o nome do arquivo atual
        self.source_code = source_code
        self.current_commit = None
        self.matches_found = []  # 

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name
                
    def set_current_file(self, filename):
        self.current_file = filename

    def set_current_commit(self, commit_hash):
        self.current_commit = commit_hash

    def visit_Match(self, node):
        if node not in getattr(self, 'visited_nodes', set()):
            if not hasattr(self, 'visited_nodes'):
                self.visited_nodes = set()
            self.visited_nodes.add(node)

            self.metrics['pattern_match'] += 1
            self.metrics['pattern_match_files'].add(self.current_file)

            code = ast.get_source_segment(self.source_code, node)

            self.matches_found.append({
                'commit': self.current_commit,
                'file': self.current_file,
                'lineno': node.lineno,
                'code': code
            })

        self.generic_visit(node)


    def visit_MatchSequence(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['pattern_sequence'] += 1
            if self.current_file not in self.metrics['pattern_sequence_files']:
                self.metrics['pattern_sequence_files'].add(self.current_file)
            for pattern in node.patterns:
                self._visit_pattern(pattern)
            print(f"\n➡ MatchClass encontrado em: {self.current_file}:{node.lineno}")
            print("Código:")
            print(ast.get_source_segment(self.source_code, node))
        self.generic_visit(node)
        
    def visit_MatchMapping(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['pattern_mapping'] += 1
            if self.current_file not in self.metrics['pattern_mapping_files']:
                self.metrics['pattern_mapping_files'].add(self.current_file)
            for pattern in node.patterns:
                self._visit_pattern(pattern)
        self.generic_visit(node)
        
    def visit_MatchClass(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['pattern_class'] += 1
            if self.current_file not in self.metrics['pattern_class_files']:
                self.metrics['pattern_class_files'].add(self.current_file)
            for pattern in node.patterns:
                self._visit_pattern(pattern)
        self.generic_visit(node)
        
    def visit_MatchAs(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['pattern_as'] += 1
            if self.current_file not in self.metrics['pattern_as_files']:
                self.metrics['pattern_as_files'].add(self.current_file)
            self.generic_visit(node)
            
    def visit_MatchOr(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['pattern_or'] += 1
            if self.current_file not in self.metrics['pattern_or_files']:
                self.metrics['pattern_or_files'].add(self.current_file)
            for pattern in node.patterns:
                self._visit_pattern(pattern)
        self.generic_visit(node)

    def _visit_pattern(self, pattern):
        # Verifica e contabiliza o tipo de padrão
        if isinstance(pattern, ast.MatchAs):
            # print(f'Encontrado node MatchAs: {ast.dump(pattern, annotate_fields=True, indent=1)}')
            self.visit_MatchAs(pattern)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchOr):
            self.visit_MatchOr(pattern)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchSequence):
            self.visit_MatchSequence(pattern)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchMapping):
            self.visit_MatchMapping(pattern)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchClass):
            self.visit_MatchClass(pattern)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchValue):
            # print(f'Encontrado node MatchValue: {ast.dump(pattern, annotate_fields=True, indent=1)}')
            self.metrics['pattern_value'] += 1
            if self.current_file not in self.metrics['pattern_value_files']:
                self.metrics['pattern_value_files'].add(self.current_file)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchSingleton):
            self.metrics['pattern_singleton'] += 1
            if self.current_file not in self.metrics['pattern_singleton_files']:
                self.metrics['pattern_singleton_files'].add(self.current_file)
            self.generic_visit(pattern)
        elif isinstance(pattern, ast.MatchStar):
            self.metrics['pattern_star'] += 1
            if self.current_file not in self.metrics['pattern_star_files']:
                self.metrics['pattern_star_files'].add(self.current_file)
            self.generic_visit(pattern)
