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
   
    def test_var_annotation(self):
        
        code = loader('tests/resources/compreension_async.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
 
        self.assertEqual(visitor.async_for, 1)
        self.assertEqual(visitor.async_with, 1)
        self.assertEqual(visitor.async_list_comprehensions, 1)
        self.assertEqual(visitor.async_set_comprehensions, 1)
        self.assertEqual(visitor.async_dict_comprehensions, 1)
        self.assertEqual(visitor.async_generator_expressions, 1)
 

if __name__ == '__main__':
    unittest.main()