import ast
import unittest
import os

from visitors.unpack_visitor import UnpackVisitor

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
                   
       
    def test_unpacking_count(self):
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
        
        
        
    # def test_unpacking_count_multiple_files(self):
        
    #     # Create a DecoratorsWithExpressionVisitor instance
    #     visitor = UnpackVisitor()
            
    #     # Create an AST node representing the code with a single With statement
    #     for file in self.get_repo_files('dataset/numpy_numpy'):  
    #         try:
    #             with open(file, 'r') as f:
    #                 code = f.read()
                                              
    #             tree = ast.parse(code)
                
    #             visitor.set_current_file(file)

    #             # Visit the AST tree
    #             visitor.visit(tree)
    #         except Exception as e:
    #             # print(f'Erro no arquivo {file}: {e}')
    #             continue
            
            
    #     print(visitor.metrics)
    #     # print(visitor.dict_context)        
    #     # Assert that the count is correct        
    #     self.assertEqual(visitor.metrics['call_args_unpack'], 2)
    #     self.assertEqual(visitor.metrics['call_kwargs_unpack'], 1)
        
    #     self.assertEqual(len(visitor.metrics['call_args_unpack_files']), 1)
    #     self.assertEqual(len(visitor.metrics['call_kwargs_unpack_files']), 1)
        
    # def get_repo_files(self, path):
    #     repo_files = []
    #     for dirpath, dirnames, files in os.walk(path):
    #         for file in files:
    #             if file.endswith('.py') and not self.should_ignore_file(os.path.join(dirpath, file)):
    #                 repo_files.append(os.path.join(dirpath, file))
    #     return repo_files
    
    # def should_ignore_file(self, file_path):
    #     ignored_files = [
    #         '__init__.py', 'setup.py'
    #     ]
    #     ignored_dirs = [
    #         'venv', 'env', '__pycache__', 'dist', 'build', 'site-packages', 'node_modules'
    #     ]
    #     # Verificar se é um arquivo ou diretório ignorado
    #     file_name = os.path.basename(file_path)
    #     dir_name = os.path.basename(os.path.dirname(file_path))

    #     return file_name in ignored_files or dir_name in ignored_dirs          
        

if __name__ == '__main__':
    unittest.main()