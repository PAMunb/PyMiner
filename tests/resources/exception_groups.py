# exception_groups_usage_examples.py

"""
Este arquivo contém diversos trechos de código que ilustram:
 1. Uso válido de ExceptionGroup com `except*`;
 2. Uso válido de ExceptionGroup com captura normal (`except ExceptionGroup`);
 3. Uso combinado em blocos separados;
 4. Formas inválidas que DEVEM ser ignoradas pelo visitor (apresentadas em literais de strings).
"""

# --- 1. Uso Válido: ExceptionGroup + except* ---

def example_except_star_single():
    from builtins import ExceptionGroup

    grp = ExceptionGroup(
        "Erros de validação",
        [ValueError("inválido"), KeyError("chave ausente")]
    )
    try:
        raise grp
    except* ValueError as e:
        print("Tratou somente ValueError:", e.exceptions)
    except* KeyError as e:
        print("Tratou somente KeyError:", e.exceptions)


def example_except_star_multiple():
    from builtins import ExceptionGroup

    grp = ExceptionGroup(
        "Múltiplos erros",
        [TypeError("tipo"), IndexError("índice"), TypeError("outro tipo")]
    )
    try:
        raise grp
    except* TypeError as e:
        print(f"TypeErrors encontrados: {len(e.exceptions)}")
    except* IndexError as e:
        print("IndexErrors capturados corretamente")

# --- 2. Uso Válido: ExceptionGroup + captura normal ---

def example_normal_except_group():
    from builtins import ExceptionGroup

    try:
        raise ExceptionGroup("Fallback genérico", [RuntimeError("fail")])
    except ExceptionGroup as eg:
        print(f"Capturou grupo inteiro com {len(eg.exceptions)} exceções")

# --- 3. Uso Combinado em blocos separados ---

def example_combined_separate_blocks():
    from builtins import ExceptionGroup

    grp = ExceptionGroup("Combinado", [ValueError("x"), KeyError("y")])
    # Primeiro bloco trata parte das exceções com except*
    try:
        raise grp
    except* ValueError as ve:
        print("Tratou ValueError:", ve.exceptions)
    # Segundo bloco trata o restante com captura normal
    try:
        raise grp
    except ExceptionGroup as eg:
        print("Tratou resto do grupo:", eg.exceptions)

# --- 4. Formas Inválidas (ignoradas pelo visitor) ---

# 4.1 Captura normal de ZeroDivisionError
# Deve ser ignorado: não envolve ExceptionGroup
invalid_1 = '''
try:
    1 / 0
except ZeroDivisionError as zde:
    print("Erro padrão capturado, sem ExceptionGroup")
'''

# 4.2 raise de exceção única
# Deve ser ignorado: não envolve ExceptionGroup
invalid_2 = '''
raise ValueError("erro único")
'''

# 4.3 except* sem ExceptionGroup
# Emitirá um AST TryStar, mas sem ExceptionGroup instanciado
invalid_3 = '''
try:
    1 + 'a'
except* TypeError:
    pass
'''

# 4.4 Mistura inválida de handlers no mesmo try
# Não é sintaticamente válido em Python 3.12+ e deve ser representado em literal de string
invalid_4 = '''
try:
    raise grp
except* ValueError:
    pass
except ValueError as e:
    pass
'''

try:
    1 + 'a'
except* TypeError:
    pass

# Fim de arquivo: apenas snippets - sem lógica de execução


"""
Diversos exemplos de uso de exceções padrão do Python que NÃO envolvem ExceptionGroup ou except*.
Servem para ilustrar casos que devem ser ignorados pelo visitor especializado.
"""

# 1. Raise e captura simples de exceções built-in

def simple_raise_and_catch():
    try:
        raise ValueError("valor inválido")
    except ValueError as e:
        print(f"Capturou ValueError: {e}")

# 2. Uso de exceções customizadas

class MyError(Exception):
    pass


def custom_exception():
    try:
        raise MyError("erro definido pelo usuário")
    except MyError as e:
        print("Erro customizado capturado")

# 3. Captura múltipla com tupla de exceções

def tuple_except():
    try:
        x = int('abc')
    except (ValueError, TypeError) as e:
        print(f"Capturou ValueError ou TypeError: {e}")

# 4. Tratamento genérico de qualquer exceção (exceto)

def catch_all_exceptions():
    try:
        open('file.txt')
    except Exception as e:
        print(f"Capturou qualquer Exception: {e}")

# 5. Bare except (captura de BaseException)

def bare_except():
    try:
        1 / 0
    except:
        print("Capturou qualquer exceção incluindo KeyboardInterrupt e SystemExit")

# 6. Uso de finally e else em bloco try/except

def try_except_else_finally():
    try:
        result = 10 / 2
    except ZeroDivisionError:
        print("Divisão por zero")
    else:
        print(f"Sucesso: {result}")
    finally:
        print("Sempre executa: limpeza de recursos")

# 7. Reencadeamento de exceções com raise from

def raise_from_chain():
    try:
        int('xyz')
    except ValueError as ve:
        raise RuntimeError("Falha na conversão") from ve

# 8. Exceções em corrotinas (async/await)

import asyncio

async def async_error():
    raise RuntimeError("Erro em async")

async def run_async_error():
    try:
        await async_error()
    except RuntimeError as e:
        print("Capturou em async:", e)

# 9. Exceções personalizadas com múltiplos parâmetros

class DataError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def raise_data_error():
    try:
        raise DataError(404, "Dado não encontrado")
    except DataError as de:
        print(f"Erro {de.code}: {de}")

# 10. Exceções de contexto de gerenciador de recursos

from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Recurso adquirido")
    try:
        yield
    finally:
        print("Recurso liberado")


def use_managed_resource():
    try:
        with managed_resource():
            raise IOError("Falha de I/O")
    except IOError as e:
        print("Capturou IOError dentro de with")


# FIM: Estes exemplos NÃO devem ser contados pelo ExceptionGroupsVisitor


