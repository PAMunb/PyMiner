import ast

class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
       # self.feature_count = 0  
        self.feature_with = 0
       # self.feature_starred = 0
       # self.feature_nonlocal = 0
       # self.feature_argument = 0
       # self.feature_list = 0
       # self.feature_dict = 0

    def visit(self, node):
            
        """if isinstance(node, ast.stmt):
            self.feature_count += 1
            # print(f'Encontrado node Statement: {ast.dump(node, annotate_fields=True, indent=4)}')
         
        #PEP 448: generalizações adicionais de descompactação   
        if isinstance(node.value, ast.List):
            self.feature_list +=1       
            
        #PEP 448: generalizações adicionais de descompactação            
        if isinstance(node.value, ast.Dict):
            self.feature_dict += 1
        """
        #PEP 3107: Essa PEP introduziu o gerenciamento de contexto em Python, utilizando o bloco with
        if isinstance(node, ast.With):
            self.feature_with += 1
        
        """
        #PEP 3102: introduziu argumentos somente por palavra-chave em Python
        if isinstance(node, ast.arguments):
            self.feature_argument += 1
        
         
        #PEP 3104: declaração não local
        if isinstance(node, ast.Nonlocal):
            self.feature_nonlocal += 1        
       
        #PEP 3132: Desempacotamento Estendido 
        if isinstance(node.targets[0], ast.Tuple):
                for target in node.targets[0].elts:
                    if isinstance(target, ast.Starred):
                        self.feature_starred += 1
                        print("Desempacotamento estendido encontrado!")
                        Analisar mais a fundo o nó
                        if isinstance(target.value, ast.Name):
                            print(f"Nome coringa: {target.value.id}")
                        elif isinstance(target.value, ast.Subscript):
                            print("Desempacotamento estendido com slicing!")
                            # Analisar o slice para ver se está sendo usado corretamente
                        else:
                            print(f"Tipo de nome coringa não reconhecido: {type(target.value)}")"""

        

        self.generic_visit(node)