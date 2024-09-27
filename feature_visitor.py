import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self): 
          
        self.feature_list_annotations = 0
        self.feature_dict_annotations = 0
        self.feature_set_annotations = 0
        self.feature_tuple_annotations = 0
        self.feature_old_typing_annotations = 0
        self.feature_collections_annotations = {
            "deque": 0,
            "Counter": 0,
            "defaultdict": 0,
            "OrderedDict": 0,
            "ChainMap": 0, #falta outros tipos tira duvida com walter
        }

    def visit_AnnAssign(self, node):
        # Verifica se a anotação é uma coleção padrão ou coleção do módulo collections
        if isinstance(node.annotation, ast.Subscript):
            if isinstance(node.annotation.value, ast.Name):
                if node.annotation.value.id == 'list':
                    self.feature_list_annotations += 1
                elif node.annotation.value.id == 'dict':
                    self.feature_dict_annotations += 1
                elif node.annotation.value.id == 'set':
                    self.feature_set_annotations += 1
                elif node.annotation.value.id == 'tuple':
                    self.feature_tuple_annotations += 1
                elif node.annotation.value.id in self.feature_collections_annotations:
                    self.feature_collections_annotations[node.annotation.value.id] += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Verifica anotações de tipo em parâmetros e retorno
        for arg in node.args.args:
            if arg.annotation and isinstance(arg.annotation, ast.Subscript):
                if isinstance(arg.annotation.value, ast.Name):
                    if arg.annotation.value.id == 'list':
                        self.feature_list_annotations += 1
                    elif arg.annotation.value.id == 'dict':
                        self.feature_dict_annotations += 1
                    elif arg.annotation.value.id == 'set':
                        self.feature_set_annotations += 1
                    elif arg.annotation.value.id == 'tuple':
                        self.feature_tuple_annotations += 1
                    elif arg.annotation.value.id in self.feature_collections_annotations:
                        self.feature_collections_annotations[arg.annotation.value.id] += 1

        if node.returns and isinstance(node.returns, ast.Subscript):
            if isinstance(node.returns.value, ast.Name):
                if node.returns.value.id == 'list':
                    self.feature_list_annotations += 1
                elif node.returns.value.id == 'dict':
                    self.feature_dict_annotations += 1
                elif node.returns.value.id == 'set':
                    self.feature_set_annotations += 1
                elif node.returns.value.id == 'tuple':
                    self.feature_tuple_annotations += 1
                elif node.returns.value.id in self.feature_collections_annotations:
                    self.feature_collections_annotations[node.returns.value.id] += 1

        # Verifica se há uso de anotações do módulo typing
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id in ['List', 'Dict', 'Set', 'Tuple', 'deque', 'Counter', 'defaultdict', 'OrderedDict', 'ChainMap']:
                    self.feature_old_typing_annotations += 1

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Verifica atribuições com coleções padrão e coleções do módulo collections
        for target in node.targets:
            if isinstance(target, ast.Name) and hasattr(node, 'annotation'):
                if isinstance(node.annotation, ast.Subscript):
                    if isinstance(node.annotation.value, ast.Name):
                        if node.annotation.value.id == 'list':
                            self.feature_list_annotations += 1
                        elif node.annotation.value.id == 'dict':
                            self.feature_dict_annotations += 1
                        elif node.annotation.value.id == 'set':
                            self.feature_set_annotations += 1
                        elif node.annotation.value.id == 'tuple':
                            self.feature_tuple_annotations += 1
                        elif node.annotation.value.id in self.feature_collections_annotations:
                            self.feature_collections_annotations[node.annotation.value.id] += 1
        self.generic_visit(node)