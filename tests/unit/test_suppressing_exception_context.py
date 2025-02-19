import ast
import unittest
import os

from visitors.suppressing_exception_context_visitor import SuppressingExceptionContextVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestSuppressingExceptionContextVisitor(unittest.TestCase):
                   
       
    def test_suppressing_exception_context_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/suppressing_exception_context.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = SuppressingExceptionContextVisitor()
        
        visitor.set_current_file('tests/resources/suppressing_exception_context.py')

        # Visit the AST tree
        visitor.visit(tree)
     
        
        self.assertEqual(visitor.metrics['suppressing_exception_context'], 3)
        
        self.assertEqual(len(visitor.metrics['suppressing_exception_context_files']), 1)

        

if __name__ == '__main__':
    unittest.main()