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
                   
    
          
    def test_coroutines_async(self):
        
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/coroutines_async.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)    
        
        
        self.assertEqual(visitor.feature_async_defs, 2)  # Deve encontrar duas funções corrotinas
        self.assertEqual(visitor.feature_await_expressions, 2)  # Deve encontrar duas expressões await
        self.assertEqual(visitor.feature_awaitable_objects, 2)  # Deve encontrar dois objetos awaitable

    
        
if __name__ == '__main__':
    unittest.main()