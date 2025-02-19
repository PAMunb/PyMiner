"""
Arquivo de Teste para Suppressing Exception Context (PEP 409)

Casos válidos (devem ser capturados):
- raise ... from None

Casos a serem ignorados:
- raise sem "from" ou com "from" apontando para uma exceção (não None)
"""

# --- Casos VÁLIDOS (capturados) ---

def valid_case_1():
    try:
        1 / 0
    except ZeroDivisionError:
        # Contexto suprimido: deve ser capturado
        raise ValueError("Erro de divisão") from None

def valid_case_2():
    try:
        int("abc")
    except ValueError:
        # Contexto suprimido: deve ser capturado
        raise TypeError("Falha na conversão de tipo") from None

class ValidExample:
    def valid_method(self):
        try:
            {}["chave_inexistente"]
        except KeyError:
            # Contexto suprimido: deve ser capturado
            raise IndexError("Índice não encontrado") from None

# --- Casos A SEREM IGNORADOS (não capturados) ---

def ignored_case_1():
    try:
        [][0]
    except IndexError:
        # Sem supressão explícita: contextos encadeados são mantidos
        raise RuntimeError("Erro de índice em lista")

def ignored_case_2():
    try:
        {}["key"]
    except KeyError as e:
        # Encadeamento com outra exceção: não é supressão
        raise AttributeError("Erro de atributo") from e

def ignored_case_3():
    try:
        5 / 0
    except ZeroDivisionError:
        # Sem cláusula "from": o contexto é automaticamente encadeado
        raise ValueError("Operação inválida")
        
if __name__ == '__main__':
    # Apenas para evitar a execução acidental dos raises durante os testes.
    print("Arquivo de teste para Suppressing Exception Context.")
