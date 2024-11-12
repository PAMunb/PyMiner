<<<<<<< HEAD:tests/unit/test_keyword_only_arguments_visitor.py
import ast
import unittest
import os

from keyword_only_arguments_visitor import KeywordOnlyArgumentsVisitor

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
=======
import ast
import unittest
import os

from feature_visitor import FeatureVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r', encoding="utf8") as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestFeatureVisitor(unittest.TestCase):

                    
    def test_annotation_expression_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/keyword_only_arguments.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct
        self.assertEqual(visitor.feature_kw_defaults, 7)
        self.assertEqual(visitor.feature_kw_args, 7)

if __name__ == '__main__':
>>>>>>> 25f2348e59769651ce74792206c698c5356b5ab5:tests/unit/test_feature_visitor.py
    unittest.main()