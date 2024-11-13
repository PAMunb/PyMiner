import ast
import unittest
import os

from matrix_multiplication_visitor import MatrixMultiplicationVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestMatrixMultiplicationVisitor(unittest.TestCase):
                   
    
          
    def test_matrix_multiplication(self):
        
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/matrix_multiplication.py')
        tree = ast.parse(code)

        # Create a MatrixMultiplicationVisitor instance
        visitor = MatrixMultiplicationVisitor()

        visitor.set_current_file('tests/resources/matrix_multiplication.py')
        
        # Visit the AST tree
        visitor.visit(tree) 
        
        self.assertEqual(visitor.metrics['matrix_multiplication'], 5)
        self.assertEqual(len(visitor.metrics['matrix_multiplication_files']), 1) 
        
if __name__ == '__main__':
    unittest.main()