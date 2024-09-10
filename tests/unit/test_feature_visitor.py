import ast
import unittest
import os

from feature_visitor import FeatureVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestFeatureVisitor(unittest.TestCase):

                    
    def test_match_count(self):
        
        
        code = loader('tests/resources/pattern_matching.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the feature_match count is correct
        self.assertEqual(visitor.feature_match, 15)
        


    def test_case_count(self):
        
        
        code = loader('tests/resources/pattern_matching.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the feature_with count is correct
        self.assertEqual(visitor.feature_case, 42)


if __name__ == '__main__':
    unittest.main()