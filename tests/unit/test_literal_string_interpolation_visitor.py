import ast
import unittest
import os

from visitors.literal_string_interpolation_visitor import LiteralStringInterpolationVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestLiteralStringInterpolationVisitor(unittest.TestCase):

                    
    def tests_literal_string_interpolation(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/fstrings.py')
        tree = ast.parse(code)

        # Create a LiteralStringInterpolationVisitor instance
        visitor = LiteralStringInterpolationVisitor()


        visitor.set_current_file('tests/resources/fstrings.py')
        # Visit the AST tree
        visitor.visit(tree)
        
        self.assertEqual(visitor.metrics['fstring'], 18)
        self.assertEqual(len(visitor.metrics['fstring_files']), 1)

if __name__ == '__main__':
    unittest.main()