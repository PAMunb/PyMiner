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

        # Visit the AST tree
        visitor.visit(tree)

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.type_hint_counts['list'], 10) 
        self.assertEqual(visitor.type_hint_counts['tuple'], 4)  
        self.assertEqual(visitor.type_hint_counts['dict'], 7) 
        self.assertEqual(visitor.type_hint_counts['set'], 4) 
        self.assertEqual(visitor.type_hint_counts['frozenset'], 4)
        self.assertEqual(visitor.type_hint_counts['type'], 3)


if __name__ == '__main__':
    unittest.main()