import ast
import unittest
import os

from visitors.assignment_expression_visitor import AssignmentExpressionVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestAssignmentExpressionVisitorVisitor(unittest.TestCase):
                   
       
    def test_assignment_expression_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/assignment_expression.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = AssignmentExpressionVisitor()
        
        visitor.set_current_file('tests/resources/assignment_expression.py')

        # Visit the AST tree
        visitor.visit(tree)
        
        self.assertEqual(visitor.metrics['assignment_expression'], 15)
        
        self.assertEqual(len(visitor.metrics['assignment_expression_files']), 1)
        

if __name__ == '__main__':
    unittest.main()