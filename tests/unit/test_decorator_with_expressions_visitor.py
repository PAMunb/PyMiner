import ast
import unittest
import os

from visitors.decorator_with_expressions_visitor import DecoratorsWithExpressionVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestDecoratorsWithExpressionVisitor(unittest.TestCase):

                    
    def test_decorator_with_expressions_count(self):
        # Create an AST node representing the code with a single With statement
        
        code = loader('tests/resources/decorator_with_expressions.py')
        tree = ast.parse(code)

        # Create a DecoratorsWithExpressionVisitor instance
        visitor = DecoratorsWithExpressionVisitor()
        
        visitor.set_current_file('tests/resources/decorator_with_expressions.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct        
        self.assertEqual(visitor.metrics['decorator_with_expressions'], 6)
        self.assertEqual(len(visitor.metrics['decorator_with_expressions_files']), 1)
        
        
        
    # def test_decorator_with_expressions_count_multiple_files(self):
        
    #     # Create a DecoratorsWithExpressionVisitor instance
    #     visitor = DecoratorsWithExpressionVisitor()
            
    #     # Create an AST node representing the code with a single With statement
    #     for file in self.get_repo_files('/home/walterlucas/Downloads/ipython'):  
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
    #     # Assert that the count is correct        
    #     self.assertEqual(visitor.metrics['decorator_with_expressions'], 0)
    #     self.assertEqual(len(visitor.metrics['decorator_with_expressions_files']), 0)
        
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