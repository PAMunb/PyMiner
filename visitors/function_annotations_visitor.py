import ast

class FunctionAnnotationsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metrics = {
            # Métricas originais
            'function_args_annotation': 0,
            'function_return_annotation': 0,
            'function_args_annotation_files': set(),
            'function_return_annotation_files': set(),

            # Novas métricas: funções que possuem algum tipo de anotação
            # (seja em args ou no return) e funções sem anotação alguma
            'function_with_annotation': 0,
            'function_with_annotation_files': set(),
            'function_without_annotation': 0,
            'function_without_annotation_files': set()
        }
        self.visited_nodes = set()  # nós únicos já visitados
        self.current_file = ""      # nome do arquivo atual

        # Dicionário para indicar se uma dada função (FunctionDef/AsyncFunctionDef)
        # tem alguma anotação (args ou retorno). Mapearemos o nó -> bool
        self.function_has_annotation = {}

        # Stack para sabermos em qual função estamos (caso haja funções aninhadas)
        self.function_stack = []

    def set_current_file(self, file_name):
        self.current_file = file_name

    # ---------------------------------------------------------
    # Captura de anotações em parâmetros (PEP 3107)
    # Cada parâmetro (arg) tem node.annotation se houver anotações
    def visit_arg(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.annotation:
                # Métrica de parâmetro anotado
                self.metrics['function_args_annotation'] += 1
                self.metrics['function_args_annotation_files'].add(self.current_file)

                # Marca a função atual (no topo da stack) como anotada
                if self.function_stack:
                    current_func = self.function_stack[-1]
                    self.function_has_annotation[current_func] = True

        self.generic_visit(node)

    # ---------------------------------------------------------
    # Funções assíncronas com anotação de retorno
    def visit_AsyncFunctionDef(self, node):
        self.function_stack.append(node)

        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Marca inicialmente como "não anotada"
            self.function_has_annotation[node] = False

            # Se tem anotação de retorno, incrementamos e marcamos
            if node.returns is not None:
                self.metrics['function_return_annotation'] += 1
                self.metrics['function_return_annotation_files'].add(self.current_file)
                self.function_has_annotation[node] = True

        # Visita o conteúdo da função (parâmetros, corpo, etc.)
        self.generic_visit(node)

        # Ao terminar, verifica se está anotada ou não
        if self.function_has_annotation[node]:
            self.metrics['function_with_annotation'] += 1
            self.metrics['function_with_annotation_files'].add(self.current_file)
        else:
            self.metrics['function_without_annotation'] += 1
            self.metrics['function_without_annotation_files'].add(self.current_file)

        self.function_stack.pop()

    # ---------------------------------------------------------
    # Funções “normais” (sincronas) com anotação de retorno
    def visit_FunctionDef(self, node):
        self.function_stack.append(node)

        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Marca inicialmente como "não anotada"
            self.function_has_annotation[node] = False

            # Se tem anotação de retorno, incrementamos e marcamos
            if node.returns is not None:
                self.metrics['function_return_annotation'] += 1
                self.metrics['function_return_annotation_files'].add(self.current_file)
                self.function_has_annotation[node] = True

        # Visita o conteúdo da função (parâmetros, corpo, etc.)
        self.generic_visit(node)

        # Ao terminar, verifica se está anotada ou não
        if self.function_has_annotation[node]:
            self.metrics['function_with_annotation'] += 1
            self.metrics['function_with_annotation_files'].add(self.current_file)
        else:
            self.metrics['function_without_annotation'] += 1
            self.metrics['function_without_annotation_files'].add(self.current_file)

        self.function_stack.pop()
