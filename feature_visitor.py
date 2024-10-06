import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.type_hint_counts = {
            'list': 0,
            'tuple': 0,
            'dict': 0,
            'set': 0,
            'frozenset': 0,
            'deque': 0,
            'defaultdict': 0,
            'OrderedDict': 0,
            'Counter': 0,
            'ChainMap': 0,
            'Awaitable': 0,
            'Coroutine': 0,
            'AsyncIterable': 0,
            'AsyncIterator': 0,
            'AsyncGenerator': 0,
            'Iterable': 0,
            'Iterator': 0,
            'Generator': 0,
            'Reversible': 0,
            'Container': 0,
            'Collection': 0,
            'Callable': 0,
            'Set': 0,
            'MutableSet': 0,
            'Mapping': 0,
            'MutableMapping': 0,
            'Sequence': 0,
            'MutableSequence': 0,
            'ByteString': 0,
            'MappingView': 0,
            'KeysView': 0,
            'ItemsView': 0,
            'ValuesView': 0,
            'AbstractContextManager': 0,
            'AbstractAsyncContextManager': 0,
            'Pattern': 0,
            'Match': 0,
        }
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
      
        
    def visit_Name(self, node):
        type_name = node.id
        if type_name in self.type_hint_counts:
            self.type_hint_counts[type_name] += 1
        self.generic_visit(node)
        
    # Ainda falta melhorar essa implementação.. pois acredito que não está cobrindo todos os casos. Outra alternativa é focar apenas nos tipos primitivos    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            # Verifica se a chamada é do módulo re
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 're':
                if node.func.attr == 'compile':
                    
                    # print(f'Encontrado node Pattern: {ast.dump(node, annotate_fields=True, indent=1)}')
                    self.type_hint_counts['Pattern'] += 1  # Captura Pattern
        self.generic_visit(node)