import ast
import unittest
import os

from nonlocal_statement_visitor import NonlocalStatementVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestNonlocalStatementVisitor(unittest.TestCase):

                    
    def test_annotation_expression_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/non_locals.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = NonlocalStatementVisitor()
        
        visitor.set_current_file('tests/resources/non_locals.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct
        self.assertEqual(visitor.metrics['nonlocal'], 7)
        self.assertEqual(len(visitor.metrics['nonlocal_files']),1)
 

if __name__ == '__main__':
    unittest.main()