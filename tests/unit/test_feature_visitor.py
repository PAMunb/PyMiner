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

                    
      def test_exception_groups_count(self):        
        
        code = loader('tests/resources/exception_groups.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        
        # Verifica o número de grupos de exceções e except*
        self.assertEqual(visitor.feature_exception_group_count, 2, "Should find 2 exception groups.")
        self.assertEqual(visitor.feature_except_star_count, 2, "Should find 2 except* blocks.")


if __name__ == '__main__':
    unittest.main()