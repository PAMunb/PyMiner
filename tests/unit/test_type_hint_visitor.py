import ast
import unittest
import os

from type_hint_visitor import TypeHintVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestTypeHintVisitor(unittest.TestCase):
   
    def test_type_hiting(self):
        
        code = loader('tests/resources/type_hiting.py')
        tree = ast.parse(code)

        # Create a TypeHintVisitor instance
        visitor = TypeHintVisitor()
        
        visitor.set_current_file("tests/resources/type_hiting.py")

        # Visit the AST tree
        visitor.visit(tree)

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.metrics['type_hint_list'], 10) 
        self.assertEqual(visitor.metrics['type_hint_tuple'], 4)  
        self.assertEqual(visitor.metrics['type_hint_dict'], 7) 
        self.assertEqual(visitor.metrics['type_hint_set'], 4) 
        self.assertEqual(visitor.metrics['type_hint_frozenset'], 4)
        self.assertEqual(visitor.metrics['type_hint_type'], 3)
        
        # Verifica se as contagens de arquivos com ocorrência estão corretas
        self.assertEqual(len(visitor.metrics['type_hint_files_list']), 1)
        self.assertEqual(len(visitor.metrics['type_hint_files_tuple']), 1)  
        self.assertEqual(len(visitor.metrics['type_hint_files_dict']), 1) 
        self.assertEqual(len(visitor.metrics['type_hint_files_set']), 1) 
        self.assertEqual(len(visitor.metrics['type_hint_files_frozenset']), 1)
        self.assertEqual(len(visitor.metrics['type_hint_files_type']), 1)
        
    def test_ignore_typing_examples(self):
        
        code = loader('tests/resources/typing_examples.py')
        tree = ast.parse(code)

        # Create a TypeHintVisitor instance
        visitor = TypeHintVisitor()
        
        visitor.set_current_file("tests/resources/typing_examples.py")

        # Visit the AST tree
        visitor.visit(tree)

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.metrics['type_hint_list'], 0) 
        self.assertEqual(visitor.metrics['type_hint_tuple'], 0)  
        self.assertEqual(visitor.metrics['type_hint_dict'], 0) 
        self.assertEqual(visitor.metrics['type_hint_set'], 0) 
        self.assertEqual(visitor.metrics['type_hint_frozenset'], 0)
        self.assertEqual(visitor.metrics['type_hint_type'], 0)
        
        # Verifica se as contagens de arquivos com ocorrência estão corretas
        self.assertEqual(len(visitor.metrics['type_hint_files_list']), 0)
        self.assertEqual(len(visitor.metrics['type_hint_files_tuple']), 0)  
        self.assertEqual(len(visitor.metrics['type_hint_files_dict']), 0) 
        self.assertEqual(len(visitor.metrics['type_hint_files_set']), 0) 
        self.assertEqual(len(visitor.metrics['type_hint_files_frozenset']), 0)
        self.assertEqual(len(visitor.metrics['type_hint_files_type']), 0)

if __name__ == '__main__':
    unittest.main()