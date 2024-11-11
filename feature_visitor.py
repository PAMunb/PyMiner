import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.type_hint_counts = {
            'list': 0,
            'tuple': 0,
            'dict': 0,
            'set': 0,
            'frozenset': 0,
            'type': 0
        }
        self.type_hint_file_counts = {
            'list': set(),
            'tuple': set(),
            'dict': set(),
            'set': set(),
            'frozenset': set(),
            'type': set()
        }
        self.visited_nodes = set()  # Conjunto para armazenar nós únicos já visitados
        self.all_stmts = 0
        self.current_file = ""  # Para armazenar o nome do arquivo atual

    def set_current_file(self, file_name):
        # Método para setar o arquivo atual
        self.current_file = file_name

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
        
    def visit_FunctionDef(self,node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.args.args:
                for arg in node.args.args:
                    if arg.annotation:
                            self.extract_annotation(arg.annotation)
            if node.returns:
                    self.extract_annotation(node.returns)
            if node.body:
                for stmt in node.body:
                    if isinstance(stmt,ast.AnnAssign):
                        self.extract_annotation(stmt)
                    if isinstance(stmt,ast.FunctionDef):
                        self.visit_FunctionDef(stmt)
                    if isinstance(stmt,ast.AsyncFunctionDef):
                        self.visit_AsyncFunctionDef(stmt)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self,node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.args.args:
                for arg in node.args.args:
                    if arg.annotation:
                        self.extract_annotation(arg.annotation)
            if node.returns:
                self.extract_annotation(node.returns)
            if node.body:
                for stmt in node.body:
                    if isinstance(stmt,ast.AnnAssign):
                        self.extract_annotation(stmt)
                    if isinstance(stmt,ast.FunctionDef):
                        self.visit_FunctionDef(stmt)
                    if isinstance(stmt,ast.AsyncFunctionDef):
                        self.visit_AsyncFunctionDef(stmt)
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            for stmt in node.body:
                if isinstance(stmt,ast.FunctionDef):
                    self.visit_FunctionDef(stmt)
                if isinstance(stmt,ast.AsyncFunctionDef):
                    self.visit_AsyncFunctionDef(stmt)
                if isinstance(stmt,ast.AnnAssign):
                    self.extract_annotation(stmt)
                if isinstance(stmt,ast.ClassDef):
                    self.visit_ClassDef(stmt)
                    
            if node.bases:
                for base in node.bases:
                    if isinstance(base, ast.Subscript):
                        # print(f'Classe com parâmetros de tipo: {ast.dump(base)}')
                        self.extract_annotation(base)
        self.generic_visit(node)
        
    def visit_Assign(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            # Verifica se a atribuição é de um type alias
            # print(f'Type aliases: {ast.dump(node)}')
            if isinstance(node.value, ast.Subscript):
                # print(f'Tipo alias detectado: {ast.dump(node)}')
                self.extract_annotation(node.value)
        self.generic_visit(node)
                    
    def visit_Module(self, node):
        if node not in self.visited_nodes:
            self.visited_nodes.add(node)
            if node.body:
                for stmt in node.body:
                    if isinstance(stmt,ast.AnnAssign):
                        self.extract_annotation(stmt)
        self.generic_visit(node)
        
    def extract_annotation(self, node):
        if isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):
                # print(f'Encontrado Subscript Annotation Id: {node.value.id}')
                type_name = node.value.id
                if type_name in self.type_hint_counts:
                    self.type_hint_counts[type_name] += 1
                    if self.current_file not in self.type_hint_file_counts[type_name]:
                        self.type_hint_file_counts[type_name].add(self.current_file)
            else:
                self.extract_annotation(node.value)
        elif isinstance(node, ast.Name):
            # print(f'Encontrado Annotation Name Id: {node.id}')            
            type_name = node.id
            if type_name in self.type_hint_counts:
                self.type_hint_counts[type_name] += 1
                if self.current_file not in self.type_hint_file_counts[type_name]:
                    self.type_hint_file_counts[type_name].add(self.current_file)
        elif isinstance(node, ast.AnnAssign):
            if node.annotation:
                self.extract_annotation(node.annotation)
        elif isinstance(node, ast.Constant):
            # Aqui tratamos o caso de anotações que são strings
            # print(f'Encontrado Annotation Name Id: {node.value}')
            if isinstance(node.value, str):
                type_name = node.value
                if type_name in self.type_hint_counts:
                    self.type_hint_counts[type_name] += 1
                    if self.current_file not in self.type_hint_file_counts[type_name]:
                        self.type_hint_file_counts[type_name].add(self.current_file)
        elif isinstance(node, ast.Attribute):
            # Aqui lidamos com anotações que são atributos de módulos
            # print(f'Encontrado Annotation Name Id: {node.value.id}.{node.attr}')
            # type_name = f'{node.value.id}.{node.attr}'
            # if type_name in self.type_hint_counts:
            #     self.type_hint_counts[type_name] += 1
            pass
                
    def print_file_counts(self):
        # Método para imprimir as contagens dos arquivos
        for type_name, files in self.type_hint_file_counts.items():
            print(f'{type_name}: {len(files)} arquivos encontrados')
            for file in files:
                print(f'  - {file}')