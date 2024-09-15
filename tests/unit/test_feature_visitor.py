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
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestFeatureVisitor(unittest.TestCase):
                   
       
    def test_list_unpacking_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)    
        
        self.assertEqual(visitor.feature_unpack_lists, 3)
        self.assertEqual(visitor.feature_unpack_tuples, 0)
        self.assertEqual(visitor.feature_unpack_dicts, 0)
        self.assertEqual(visitor.feature_call_unpack_args, 0)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 0)

    def test_tuple_unpacking_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)      

        
        self.assertEqual(visitor.feature_unpack_lists, 0)
        self.assertEqual(visitor.feature_unpack_tuples, 4)
        self.assertEqual(visitor.feature_unpack_dicts, 0)
        self.assertEqual(visitor.feature_call_unpack_args, 0)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 0)

    def test_dict_unpacking_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)
       
        
        self.assertEqual(visitor.feature_unpack_lists, 0)
        self.assertEqual(visitor.feature_unpack_tuples, 0)
        self.assertEqual(visitor.feature_unpack_dicts, 1)
        self.assertEqual(visitor.feature_call_unpack_args, 0)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 0)

    def test_call_unpacking_args_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)
       
        self.assertEqual(visitor.feature_unpack_lists, 0)
        self.assertEqual(visitor.feature_unpack_tuples, 0)
        self.assertEqual(visitor.feature_unpack_dicts, 0)
        self.assertEqual(visitor.feature_call_unpack_args, 1)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 0)

    def test_call_unpacking_kwargs_count(self):
        
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)
        self.assertEqual(visitor.feature_unpack_lists, 0)
        self.assertEqual(visitor.feature_unpack_tuples, 0)
        self.assertEqual(visitor.feature_unpack_dicts, 0)
        self.assertEqual(visitor.feature_call_unpack_args, 0)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 1)

    def test_no_unpacking(self):
        
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)
        
        self.assertEqual(visitor.feature_unpack_lists, 0)
        self.assertEqual(visitor.feature_unpack_tuples, 0)
        self.assertEqual(visitor.feature_unpack_dicts, 0)
        self.assertEqual(visitor.feature_call_unpack_args, 0)
        self.assertEqual(visitor.feature_call_unpack_kwargs, 0)

    def test_incomplete_unpacking(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)
      
        self.assertEqual(visitor.feature_unpack_lists, 1)
        

if __name__ == '__main__':
    unittest.main()