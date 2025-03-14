import ast
import unittest
import os

from visitors.variable_annotations_visitor import VariableAnnotationsVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestVariableAnnotationsVisitorVisitor(unittest.TestCase):
                   
       
    def test_variable_annotations_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/variable_annotation.py')
        tree = ast.parse(code, type_comments=True)

        # Create a FeatureVisitor instance
        visitor = VariableAnnotationsVisitor()
        
        visitor.set_current_file('tests/resources/variable_annotation.py')

        # Visit the AST tree
        visitor.visit(tree)
     
        
        self.assertEqual(visitor.metrics['variable_annotation'], 9)
        
        self.assertEqual(len(visitor.metrics['variable_annotation_files']), 1)
        
        
    def test_assign_augassign_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/assign_augassign.py')
        tree = ast.parse(code, type_comments=True)

        # Create a FeatureVisitor instance
        visitor = VariableAnnotationsVisitor()
        
        visitor.set_current_file('tests/resources/assign_augassign.py')

        # Visit the AST tree
        visitor.visit(tree)

       
        self.assertEqual(visitor.metrics['assign'], 4)
        self.assertEqual(visitor.metrics['assign_with_type_comment'], 2)
        self.assertEqual(visitor.metrics['aug_assign'], 3)
        
        self.assertEqual(len(visitor.metrics['assign_files']), 1)
        self.assertEqual(len(visitor.metrics['assign_with_type_comment_files']), 1)
        self.assertEqual(len(visitor.metrics['aug_assign_files']), 1)

        

if __name__ == '__main__':
    unittest.main()