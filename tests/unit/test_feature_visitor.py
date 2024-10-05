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
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestFeatureVisitor(unittest.TestCase):
                   
       
    def test_list_unpacking_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)    
        
        self.assertEqual(visitor.feature_unpacking_generalizations, 26)
        

if __name__ == '__main__':
    unittest.main()