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
   
    def test_type_hiting(self):
        
        code = loader('tests/resources/type_hiting.py')
        tree = ast.parse(code)

        # Create a FeatureVisitor instance
        visitor = FeatureVisitor()

        # Visit the AST tree
        visitor.visit(tree)

        # Verifica se as contagens estão corretas
        self.assertEqual(visitor.type_hint_counts['list'], 9)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['tuple'], 1)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['dict'], 4)   # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['set'], 3)    # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['frozenset'], 2)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['deque'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['defaultdict'], 2)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['OrderedDict'], 2)   # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Counter'], 2)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['ChainMap'], 2)       # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Awaitable'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Coroutine'], 2)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['AsyncIterable'], 1)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['AsyncIterator'], 1)   # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['AsyncGenerator'], 1)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Iterable'], 1)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Iterator'], 1)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Generator'], 1)       # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Reversible'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Container'], 1)       # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Collection'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Callable'], 1)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Set'], 1)             # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['MutableSet'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Mapping'], 1)         # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['MutableMapping'], 1)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Sequence'], 1)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['MutableSequence'], 1) # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['ByteString'], 2)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['MappingView'], 1)     # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['KeysView'], 1)        # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['ItemsView'], 1)       # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['ValuesView'], 1)      # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['AbstractContextManager'], 2)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['AbstractAsyncContextManager'], 2)  # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Pattern'], 3)         # Exemplo: altere conforme esperado
        self.assertEqual(visitor.type_hint_counts['Match'], 1)           # Exemplo: altere conforme esperado


if __name__ == '__main__':
    unittest.main()