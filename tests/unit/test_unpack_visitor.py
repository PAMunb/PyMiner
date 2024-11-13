import ast
import unittest
import os

from unpack_visitor import UnpackVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print('Erro no arquivo %s: %s' % (file, e))


    return file_content

class TestUnpackVisitor(unittest.TestCase):
                   
       
    def test_list_unpacking_count(self):
         # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/add_unpacking.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = UnpackVisitor()
        
        visitor.set_current_file('tests/resources/add_unpacking.py')

        # Visit the AST tree
        visitor.visit(tree)
     
        
        self.assertEqual(visitor.metrics['assign_unpack'], 4)
        self.assertEqual(visitor.metrics['list_unpack'], 1)
        self.assertEqual(visitor.metrics['tuple_unpack'], 1)
        self.assertEqual(visitor.metrics['set_unpack'], 1)
        self.assertEqual(visitor.metrics['dict_unpack'], 1)
        self.assertEqual(visitor.metrics['call_args_unpack'], 1)
        self.assertEqual(visitor.metrics['call_kwargs_unpack'], 1)
        
        self.assertEqual(len(visitor.metrics['assign_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['list_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['tuple_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['set_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['dict_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['call_args_unpack_files']), 1)
        self.assertEqual(len(visitor.metrics['call_kwargs_unpack_files']), 1)
        

if __name__ == '__main__':
    unittest.main()