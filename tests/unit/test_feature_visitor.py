import ast
import unittest
import os

from feature_visitor import FeatureVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestFeatureVisitor(unittest.TestCase):
   
    def test_type_hiting(self):
        
        code = loader('tests/resources/type_hiting.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()
        
        visitor.set_current_file("tests/resources/type_hiting.py")

        # Visit the AST tree
        visitor.visit(tree)    

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.type_hint_counts['list'], 10) 
        self.assertEqual(visitor.type_hint_counts['tuple'], 4)  
        self.assertEqual(visitor.type_hint_counts['dict'], 7) 
        self.assertEqual(visitor.type_hint_counts['set'], 4) 
        self.assertEqual(visitor.type_hint_counts['frozenset'], 4)
        self.assertEqual(visitor.type_hint_counts['type'], 3)
        
        # Verifica se as contagens de arquivos com ocorrência estão corretas
        self.assertEqual(len(visitor.type_hint_file_counts['list']), 1)
        self.assertEqual(len(visitor.type_hint_file_counts['tuple']), 1)  
        self.assertEqual(len(visitor.type_hint_file_counts['dict']), 1) 
        self.assertEqual(len(visitor.type_hint_file_counts['set']), 1) 
        self.assertEqual(len(visitor.type_hint_file_counts['frozenset']), 1)
        self.assertEqual(len(visitor.type_hint_file_counts['type']), 1)
        
    def test_ignore_typing_examples(self):
        
        code = loader('tests/resources/typing_examples.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()
        
        visitor.set_current_file("tests/resources/typing_examples.py")

        # Visit the AST tree
        visitor.visit(tree)

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.type_hint_counts['list'], 0) 
        self.assertEqual(visitor.type_hint_counts['tuple'], 0)  
        self.assertEqual(visitor.type_hint_counts['dict'], 0) 
        self.assertEqual(visitor.type_hint_counts['set'], 0) 
        self.assertEqual(visitor.type_hint_counts['frozenset'], 0)
        self.assertEqual(visitor.type_hint_counts['type'], 0)
        
        # Verifica se as contagens de arquivos com ocorrência estão corretas
        self.assertEqual(len(visitor.type_hint_file_counts['list']), 0)
        self.assertEqual(len(visitor.type_hint_file_counts['tuple']), 0)  
        self.assertEqual(len(visitor.type_hint_file_counts['dict']), 0) 
        self.assertEqual(len(visitor.type_hint_file_counts['set']), 0) 
        self.assertEqual(len(visitor.type_hint_file_counts['frozenset']), 0)
        self.assertEqual(len(visitor.type_hint_file_counts['type']), 0)

if __name__ == '__main__':
    unittest.main()