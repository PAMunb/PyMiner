import ast
import unittest
import os

from visitors.type_parameter_visitor import TypeParameterVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestTypeParameterVisitor(unittest.TestCase):
   
    def test_type_stmt(self):
        
        code = loader('tests/resources/type_parameters.py')
        tree = ast.parse(code)

        # Create a TypeParameterVisitor instance
        visitor = TypeParameterVisitor()
        
        visitor.set_current_file("tests/resources/type_parameters.py")

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the count is correct  
        self.assertEqual(visitor.metrics['type_vars_constraints'], 3) 
        self.assertEqual(visitor.metrics['type_vars_bounds'], 4) 
        self.assertEqual(visitor.metrics['type_param_spec'], 1) 
        self.assertEqual(visitor.metrics['type_var_tuple'],1)
        self.assertEqual(visitor.metrics['type_alias'],11)
        
        self.assertEqual(len(visitor.metrics['type_vars_constraints_files']), 1) 
        self.assertEqual(len(visitor.metrics['type_vars_bounds_files']), 1) 
        self.assertEqual(len(visitor.metrics['type_param_spec_files']), 1) 
        self.assertEqual(len(visitor.metrics['type_var_tuple_files']),1)
        self.assertEqual(len(visitor.metrics['type_alias_files']),1)

if __name__ == '__main__':
    unittest.main()