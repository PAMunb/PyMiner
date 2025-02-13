import ast

class UnionOperatorsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            'dict_union': 0,
            'dict_union_update': 0,
            'dict_union_files': set(),
            'dict_union_update_files': set()
        }
        self.visited_nodes = set()
        self.current_file = ""

    def set_current_file(self, file_name):
        self.current_file = file_name

    def visit_BinOp(self, node):
        """Captura `dict | dict`, sem análise dinâmica."""
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)

            if isinstance(node.op, ast.BitOr):  # Operação `|`
                if self.is_explicit_dict(node.left) and self.is_explicit_dict(node.right):
                    print(f'✅ Encontrado dict_union: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.metrics['dict_union'] += 1
                    self.metrics['dict_union_files'].add(self.current_file)
                else:
                    print(f"⚠️ Ignorando `{ast.dump(node)}` pois os operandos não são dicionários explícitos.")

        self.generic_visit(node)

    def visit_AugAssign(self, node):
        """Captura `dict |= dict`, sem análise dinâmica."""
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)

            if isinstance(node.op, ast.BitOr):  # Operação `|=`
                if self.is_explicit_dict(node.target) and self.is_explicit_dict(node.value):
                    print(f'✅ Encontrado dict_union_update: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.metrics['dict_union_update'] += 1
                    self.metrics['dict_union_update_files'].add(self.current_file)
                else:
                    print(f"⚠️ Ignorando `{ast.dump(node)}` pois os operandos não são dicionários explícitos.")

        self.generic_visit(node)

    def is_explicit_dict(self, node):
        """Verifica se um nó da AST representa um dicionário explicitamente."""
        if isinstance(node, ast.Dict):  # Literal `{}`
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
            return True
        if isinstance(node, ast.DictComp):  # Compreensão de dicionário `{k: v for ...}`
            return True
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            return self.is_explicit_dict(node.left) and self.is_explicit_dict(node.right)
        return False
