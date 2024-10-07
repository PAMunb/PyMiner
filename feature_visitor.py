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
        self.all_stmts = 0

    def generic_visit(self, node):
        # Chama o método de visitação adequado para cada tipo de nó
        if isinstance(node, ast.stmt):
            # print(f'Encontrado node Stmt: {ast.dump(node, annotate_fields=True, indent=1)}')
            self.all_stmts += 1
        super().generic_visit(node)
        
    def visit_FunctionDef(self,node):
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
        # self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self,node):
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
        # self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        for stmt in node.body:
            if isinstance(stmt,ast.FunctionDef):
                self.visit_FunctionDef(stmt)
            if isinstance(stmt,ast.AsyncFunctionDef):
                self.visit_AsyncFunctionDef(stmt)
            if isinstance(stmt,ast.AnnAssign):
                self.extract_annotation(stmt)
            if isinstance(stmt,ast.ClassDef):
                self.visit_ClassDef(stmt)
        # self.generic_visit(node)
        
    def visit_Module(self, node):
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
        elif isinstance(node, ast.Name):
            # print(f'Encontrado Annotation Name Id: {node.id}')
            type_name = node.id
            if type_name in self.type_hint_counts:
                self.type_hint_counts[type_name] += 1
        elif isinstance(node, ast.AnnAssign):
            if node.annotation:
                self.extract_annotation(node.annotation)