import ast
import unittest
import os

from union_operators_visitor import UnionOperatorsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestUnionOperatorsVisitor(unittest.TestCase):

                    
    def test_union_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/union_operators.py')
        tree = ast.parse(code)

        # Create a UnionOperatorsVisitor instance
        visitor = UnionOperatorsVisitor()
        
        visitor.set_current_file('tests/resources/union_operators.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct
        self.assertEqual(visitor.metrics['dict_union'], 5)
        self.assertEqual(visitor.metrics['dict_union_update'], 3)
        
        self.assertEqual(len(visitor.metrics['dict_union_files']), 1)
        self.assertEqual(len(visitor.metrics['dict_union_update_files']), 1)

if __name__ == '__main__':
    unittest.main()