import ast
import unittest
import os

from visitors.yield_from_visitor import YieldFromVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestYieldFromVisitor(unittest.TestCase):
                   
       
    def test_yield_from_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/yield_from.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = YieldFromVisitor()
        
        visitor.set_current_file('tests/resources/yield_from.py')

        # Visit the AST tree
        visitor.visit(tree)
     
        
        self.assertEqual(visitor.metrics['yield_from'], 2)
        
        self.assertEqual(len(visitor.metrics['yield_from_files']), 1)

        

if __name__ == '__main__':
    unittest.main()