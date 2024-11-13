import ast
import unittest
import os

from visitors.coroutines_visitor import CoroutinesVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestCoroutinesVisitor(unittest.TestCase):
                   
    
          
    def test_coroutines_async(self):
        
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/coroutines_async.py')
        tree = ast.parse(code)

        # Create a CoroutinesVisitor instance
        visitor = CoroutinesVisitor()
        
        visitor.set_current_file('tests/resources/coroutines_async.py')

        # Visit the AST tree
        visitor.visit(tree)

        
        self.assertEqual(visitor.metrics['async_def'], 15)
        self.assertEqual(visitor.metrics['async_for'], 3)
        self.assertEqual(visitor.metrics['async_with'], 2)
        self.assertEqual(visitor.metrics['await_expressions'], 15)
        
        self.assertEqual(len(visitor.metrics['async_def_files']), 1)
        self.assertEqual(len(visitor.metrics['async_for_files']), 1)
        self.assertEqual(len(visitor.metrics['async_with_files']), 1)
        self.assertEqual(len(visitor.metrics['await_expressions_files']), 1)
        
if __name__ == '__main__':
    unittest.main()