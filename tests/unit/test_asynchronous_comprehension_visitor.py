import ast
import unittest
import os

from visitors.asynchronous_comprehension_visitor import AsynchronousComprehensionVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestAsynchronousComprehensionVisitor(unittest.TestCase):
   
    def test_var_annotation(self):
        
        code = loader('tests/resources/asynchronous_comprehension.py')
        tree = ast.parse(code)

        # Create a AsynchronousComprehensionVisitor instance
        visitor = AsynchronousComprehensionVisitor()
        
        visitor.set_current_file('tests/resources/asynchronous_comprehension.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
        self.assertEqual(visitor.metrics['async_list_comprehensions'], 1)
        self.assertEqual(visitor.metrics['async_set_comprehensions'], 1)
        self.assertEqual(visitor.metrics['async_dict_comprehensions'], 1)
        self.assertEqual(visitor.metrics['async_generator_expressions'], 1)
        
        self.assertEqual(len(visitor.metrics['async_list_comprehensions_files']), 1)
        self.assertEqual(len(visitor.metrics['async_set_comprehensions_files']), 1)
        self.assertEqual(len(visitor.metrics['async_dict_comprehensions_files']), 1)
        self.assertEqual(len(visitor.metrics['async_generator_expressions_files']), 1)

if __name__ == '__main__':
    unittest.main()