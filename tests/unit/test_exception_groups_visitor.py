import ast
import unittest
import os

from visitors.exception_groups_visitor import ExceptionGroupsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestExceptionGroupsVisitor(unittest.TestCase):

                    
      def test_exception_groups_count(self):        
        
        code = loader('tests/resources/exception_groups.py')
        tree = ast.parse(code)

        # Create a ExceptionGroupsVisitor instance
        visitor = ExceptionGroupsVisitor()
        
        visitor.set_current_file('tests/resources/exception_groups.py')

        # Visit the AST tree
        visitor.visit(tree)   

        # Assert that the feature_with count is correct
        self.assertEqual(visitor.metrics['except_star'], 6)
        self.assertEqual(len(visitor.metrics['except_star_files']), 1)


if __name__ == '__main__':
    unittest.main()