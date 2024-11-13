import ast
import unittest
import os

from visitors.underscores_numeric_literals_visitor import UnderscoresNumericLiteralsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestUnderscoresNumericLiteralsVisitor(unittest.TestCase):

                    
    def test_num_literals_count(self):
        
        code = loader('tests/resources/num_literals.py')
        tree = ast.parse(code)

        # Create a UnderscoresNumericLiteralsVisitor instance
        visitor = UnderscoresNumericLiteralsVisitor(code)

        visitor.set_current_file('tests/resources/num_literals.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
        self.assertEqual(visitor.metrics['underscores_num_literals'], 15)
        self.assertEqual(len(visitor.metrics['underscores_num_literals_files']), 1)
       
 
if __name__ == '__main__':
    unittest.main()