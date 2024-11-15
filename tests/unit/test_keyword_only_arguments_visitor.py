import ast
import unittest
import os

from visitors.keyword_only_arguments_visitor import KeywordOnlyArgumentsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestKeywordOnlyArgumentsVisitor(unittest.TestCase):

                    
    def test_annotation_expression_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/keyword_only_arguments.py')
        tree = ast.parse(code)

        # Create a KeywordOnlyArgumentsVisitor instance
        visitor = KeywordOnlyArgumentsVisitor()
        
        visitor.set_current_file('tests/resources/keyword_only_arguments.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct
        self.assertEqual(visitor.metrics['kw_defaults'], 7)
        self.assertEqual(visitor.metrics['kw_args'], 7)
        
        self.assertEqual(len(visitor.metrics['kw_defaults_files']), 1)
        self.assertEqual(len(visitor.metrics['kw_args_files']), 1)

if __name__ == '__main__':
    unittest.main()