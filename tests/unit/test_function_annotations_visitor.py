import ast
import unittest
import os

from visitors.function_annotations_visitor import FunctionAnnotationsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestFunctionAnnotationsVisitor(unittest.TestCase):

                    
    def test_function_annotation_expression_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/annotation_expression.py')
        tree = ast.parse(code)

        # Create a FunctionAnnotationsVisitor instance
        visitor = FunctionAnnotationsVisitor()
        
        visitor.set_current_file('tests/resources/annotation_expression.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the feature_with count is correct
        self.assertEqual(visitor.metrics['function_args_annotation'], 15)
        self.assertEqual(visitor.metrics['function_return_annotation'], 10)
        self.assertEqual(len(visitor.metrics['function_args_annotation_files']), 1)
        self.assertEqual(len(visitor.metrics['function_return_annotation_files']), 1)


if __name__ == '__main__':
    unittest.main()