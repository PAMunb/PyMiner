import ast
import unittest
import os

from visitors.decorator_with_expressions_visitor import DecoratorsWithExpressionVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestDecoratorsWithExpressionVisitor(unittest.TestCase):

                    
    def test_union_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/decorator_with_expressions.py')
        tree = ast.parse(code)

        # Create a DecoratorsWithExpressionVisitor instance
        visitor = DecoratorsWithExpressionVisitor()
        
        visitor.set_current_file('tests/resources/decorator_with_expressions.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
        self.assertEqual(visitor.metrics['decorator_with_expressions'], 12)
        self.assertEqual(len(visitor.metrics['decorator_with_expressions_files']), 1)

if __name__ == '__main__':
    unittest.main()