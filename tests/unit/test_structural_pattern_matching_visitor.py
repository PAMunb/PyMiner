import ast
import unittest
import os

from structural_pattern_matching_visitor import StructuralPatternMatchingVisitor

path = os.getcwd()

def loader(file):
    file_content = ''
    try:
        with open(path+"/"+file, 'r') as f:
            file_content = f.read()                          
    except Exception as e:
        print(f'Erro no arquivo {file}: {e}')
    return file_content


class TestStructuralPatternMatchingVisitor(unittest.TestCase):

                    
    def test_structural_pattern_matchs(self):
        
        
        code = loader('tests/resources/structural_pattern_matchs.py')
        tree = ast.parse(code)

        # Create a StructuralPatternMatchingVisitor instance
        visitor = StructuralPatternMatchingVisitor()
        
        visitor.set_current_file('tests/resources/structural_pattern_matchs.py')

        # Visit the AST tree
        visitor.visit(tree) 

        # Assert that the feature_match count is correct
        self.assertEqual(visitor.metrics['structural_pattern_match'], 10)
        self.assertEqual(visitor.metrics['pattern_as'], 12)
        self.assertEqual(visitor.metrics['pattern_or'], 1)
        self.assertEqual(visitor.metrics['pattern_sequence'], 3)
        self.assertEqual(visitor.metrics['pattern_mapping'], 1)
        self.assertEqual(visitor.metrics['pattern_class'], 1)
        self.assertEqual(visitor.metrics['pattern_value'], 4)
        self.assertEqual(visitor.metrics['pattern_singleton'], 1)
        self.assertEqual(visitor.metrics['pattern_star'], 2)
        
        self.assertEqual(len(visitor.metrics['structural_pattern_match_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_as_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_or_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_sequence_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_mapping_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_class_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_value_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_singleton_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_star_files']), 1)
        
    def test_pattern_matching(self):
        
        
        code = loader('tests/resources/pattern_matching.py')
        tree = ast.parse(code)

        # Create a StructuralPatternMatchingVisitor instance
        visitor = StructuralPatternMatchingVisitor()
        
        visitor.set_current_file('tests/resources/pattern_matching.py')

        # Visit the AST tree
        visitor.visit(tree)

        # Assert that the feature_match count is correct
        self.assertEqual(visitor.metrics['structural_pattern_match'], 15)
        self.assertEqual(visitor.metrics['pattern_as'], 36)
        self.assertEqual(visitor.metrics['pattern_or'], 2)
        self.assertEqual(visitor.metrics['pattern_sequence'], 6)
        self.assertEqual(visitor.metrics['pattern_mapping'], 4)
        self.assertEqual(visitor.metrics['pattern_class'], 3)
        self.assertEqual(visitor.metrics['pattern_value'], 12)
        self.assertEqual(visitor.metrics['pattern_singleton'], 4)
        self.assertEqual(visitor.metrics['pattern_star'], 1)
        
        self.assertEqual(len(visitor.metrics['structural_pattern_match_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_as_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_or_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_sequence_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_mapping_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_class_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_value_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_singleton_files']), 1)
        self.assertEqual(len(visitor.metrics['pattern_star_files']), 1)

if __name__ == '__main__':
    unittest.main()