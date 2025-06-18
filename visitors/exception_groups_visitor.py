import ast

class ExceptionGroupsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'except_star': 0,
            'except_star_with_group': 0,
            'except_star_without_group': 0,
            'raised_exception_group': 0,
            'caught_exception_group': 0,
            'exception_groups': 0,
            'except_star_files': set(),
            'exception_group_files': set()
        }
        self.visited_nodes = set()
        self.current_file = ""
        self.exceptiongroup_vars = set()

    def set_current_file(self, file_name):
        self.current_file = file_name

    def visit_Assign(self, node):
        # Registra variáveis atribuídas a ExceptionGroup(...)
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id == 'ExceptionGroup':
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.exceptiongroup_vars.add(target.id)
        self.generic_visit(node)

    def _contains_exceptiongroup_raise(self, node):
        # Verifica se há raise ExceptionGroup(...) ou raise var_de_grupo dentro do try
        for n in ast.walk(node):
            if isinstance(n, ast.Raise):
                exc = n.exc
                if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == 'ExceptionGroup':
                    return True
                if isinstance(exc, ast.Name) and exc.id in self.exceptiongroup_vars:
                    return True
        return False

    def visit_TryStar(self, node):
        # Métrica sintática: conta todo except*
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            self.metrics['except_star'] += 1
            self.metrics['except_star_files'].add(self.current_file)
            # Métricas semânticas: distingue com/sem ExceptionGroup
            if self._contains_exceptiongroup_raise(node):
                self.metrics['except_star_with_group'] += 1
                self.metrics['exception_groups'] += 1
                self.metrics['exception_group_files'].add(self.current_file)
            else:
                self.metrics['except_star_without_group'] += 1
        self.generic_visit(node)

    def visit_Raise(self, node):
        exc = node.exc
        # Captura ambos: chamadas diretas e variáveis de ExceptionGroup
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == 'ExceptionGroup':
            if node not in self.visited_nodes:
                self.visited_nodes.add(node)
                self.metrics['raised_exception_group'] += 1
                self.metrics['exception_groups'] += 1
                self.metrics['exception_group_files'].add(self.current_file)
        if isinstance(exc, ast.Name) and exc.id in self.exceptiongroup_vars:
            if node not in self.visited_nodes:
                self.visited_nodes.add(node)
                self.metrics['raised_exception_group'] += 1
                self.metrics['exception_groups'] += 1
                self.metrics['exception_group_files'].add(self.current_file)
        self.generic_visit(node)

    def visit_Try(self, node):
        # Captura except ExceptionGroup (sem *)
        for handler in node.handlers:
            t = handler.type
            if isinstance(t, ast.Name) and t.id == 'ExceptionGroup' and not getattr(handler, 'star', False):
                if handler not in self.visited_nodes:
                    self.visited_nodes.add(handler)
                    self.metrics['caught_exception_group'] += 1
                    self.metrics['exception_groups'] += 1
                    self.metrics['exception_group_files'].add(self.current_file)
        self.generic_visit(node)
