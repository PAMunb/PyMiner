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

                    
    def test_union_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/union_dict.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
        self.assertEqual(visitor.feature_simple_decorators, 1)
        self.assertEqual(visitor.feature_complex_decorators, 2)
 

if __name__ == '__main__':
    unittest.main()