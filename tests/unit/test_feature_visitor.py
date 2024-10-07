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
   
    def test_type_stmt(self):
        
        code = loader('tests/resources/type_stmt.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct  
        self.assertEqual(visitor.feature_type_vars_constraints, 3) 
        self.assertEqual(visitor.feature_type_vars_bounds, 4) 
        self.assertEqual(visitor.feature_type_param_spec, 1) 
        self.assertEqual(visitor.feature_type_var_tuple,1)
        self.assertEqual(visitor.feature_type_alias,11)

if __name__ == '__main__':
    unittest.main()