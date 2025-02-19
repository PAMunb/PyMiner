"""
Arquivo de Teste para PEP 380 - Delegando para um Subgerador

Casos VÁLIDOS (devem ser capturados):
- Uso de "yield from" para delegar a iteração a um subgerador ou a um iterador.

Casos a SEREM IGNORADOS:
- Geradores que utilizam somente "yield" individualmente.
- Funções que não são geradores.
"""

# --- Casos VÁLIDOS (capturados) ---

def valid_generator_1():
    # Exemplo de delegação usando um subgerador
    def subgen():
        for i in range(3):
            yield i
    # A delegação com yield from deve ser capturada
    yield from subgen()

def valid_generator_2():
    # Delegando para um gerador de compreensão
    yield from (x for x in range(5))

# --- Casos A SEREM IGNORADOS (não capturados) ---

def ignored_generator_1():
    # Gerador que utiliza somente yield individualmente
    for i in range(3):
        yield i

def ignored_function():
    # Função comum que não é um gerador
    return sum([1, 2, 3])

if __name__ == '__main__':
    print("Arquivo de teste para PEP 380 - Yield From")
