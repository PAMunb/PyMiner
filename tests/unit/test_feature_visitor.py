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
   
    def test_var_annotation(self):
        
        code = loader('tests/resources/compreension_async.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct  
        #self.assertEqual(visitor.feature_collections_annotations, 1) 
        self.assertEqual(visitor.feature_list_annotations, 1) 
        self.assertEqual(visitor.feature_dict_annotations, 1) 
        self.assertEqual(visitor.feature_set_annotations, 1)
       # self.assertEqual(visitor.feature_old_typing_annotations, 1)  
        self.assertEqual(visitor.feature_tuple_annotations, 1) 

if __name__ == '__main__':
    unittest.main()