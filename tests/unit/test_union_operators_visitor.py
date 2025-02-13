import ast
import unittest
import os

from visitors.union_operators_visitor import UnionOperatorsVisitor

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

                    
    # def test_union_count(self):
    #     # Create an AST node representing the code with a single With statement
        
    #     code = loader('tests/resources/union_operators.py')
    #     tree = ast.parse(code)

    #     # Create a UnionOperatorsVisitor instance
    #     visitor = UnionOperatorsVisitor()
        
    #     visitor.set_current_file('tests/resources/union_operators.py')

    #     # Visit the AST tree
    #     visitor.visit(tree)

    #     # Assert that the count is correct
    #     self.assertEqual(visitor.metrics['dict_union'], 5)
    #     self.assertEqual(visitor.metrics['dict_union_update'], 3)
        
    #     self.assertEqual(len(visitor.metrics['dict_union_files']), 1)
    #     self.assertEqual(len(visitor.metrics['dict_union_update_files']), 1)
        
        
        
    def test_union_count_multiple_files(self):
        
        # Create a DecoratorsWithExpressionVisitor instance
        visitor = UnionOperatorsVisitor()
            
        # Create an AST node representing the code with a single With statement
        for file in self.get_repo_files('dataset/sympy'):  
            try:
                with open(file, 'r') as f:
                    code = f.read()
                                              
                tree = ast.parse(code)
                
                visitor.set_current_file(file)

                # Visit the AST tree
                visitor.visit(tree)
            except Exception as e:
                # print(f'Erro no arquivo {file}: {e}')
                continue
            
            
        print(visitor.metrics)
        # print(visitor.dict_context)        
        # Assert that the count is correct        
        self.assertEqual(visitor.metrics['dict_union'], 0)
        self.assertEqual(visitor.metrics['dict_union_update'], 0)
        
        self.assertEqual(len(visitor.metrics['dict_union_files']), 0)
        self.assertEqual(len(visitor.metrics['dict_union_update_files']), 0)
        
    def get_repo_files(self, path):
        repo_files = []
        for dirpath, dirnames, files in os.walk(path):
            for file in files:
                if file.endswith('.py') and not self.should_ignore_file(os.path.join(dirpath, file)):
                    repo_files.append(os.path.join(dirpath, file))
        return repo_files
    
    def should_ignore_file(self, file_path):
        ignored_files = [
            '__init__.py', 'setup.py'
        ]
        ignored_dirs = [
            'venv', 'env', '__pycache__', 'dist', 'build', 'site-packages', 'node_modules'
        ]
        # Verificar se é um arquivo ou diretório ignorado
        file_name = os.path.basename(file_path)
        dir_name = os.path.basename(os.path.dirname(file_path))

        return file_name in ignored_files or dir_name in ignored_dirs    

if __name__ == '__main__':
    unittest.main()