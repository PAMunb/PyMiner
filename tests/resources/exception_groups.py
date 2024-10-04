
# Exemplo de uso de try* com except*
try:
    raise ValueError("Erro de valor")
except* ValueError as e:
    print("Tratando ValueError com except*:", e)

# Exemplo de uso de try* com múltiplas exceções
try:
    raise (ValueError("Erro de valor"), KeyError("Erro de chave"))
except* (ValueError, KeyError) as e:
    print("Tratando múltiplas exceções com except*:", e)

# Exemplo de uso de try* sem exceções
try:
    print("Nenhum erro ocorreu.")
except* Exception as e:
    print("Tratando erro com except*:", e)

# Exemplo de uso de try normal com except
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print("Erro de divisão por zero:", e)

# Exemplo de uso de try normal com múltiplos except
try:
    x = int("não é um número")
except ValueError as e:
    print("Erro de conversão:", e)
except TypeError as e:
    print("Erro de tipo:", e)

# Exemplo de uso de try normal sem exceções
try:
    print("Executando sem problemas.")
except Exception as e:
    print("Tratando erro com except:", e)
    
   
def process_value(value):
    if value < 0:
        raise ValueError("Valor não pode ser negativo.")
    elif value == 0:
        raise ZeroDivisionError("Divisão por zero.")
    else:
        return 10 / value

values = [-1, 0, 5]

for val in values:
    try:
        result = process_value(val)
        print(f"Resultado: {result}")
    except* (ValueError, ZeroDivisionError) as e:
        print(f"Erro: {e}")
        
class CustomError1(Exception):
    pass

class CustomError2(Exception):
    pass

class CustomError3(Exception):
    pass

def funcao_de_teste(erro):
    # Simulando a possibilidade de levantar diferentes exceções
    if erro == 1:
        raise CustomError1("Erro personalizado 1")
    elif erro == 2:
        raise CustomError2("Erro personalizado 2")
    elif erro == 3:
        raise CustomError3("Erro personalizado 3")

try:
    # Aqui você pode adicionar código que pode levantar exceções
    funcao_de_teste(1)  # Mude o argumento para 1, 2 ou 3 para testar diferentes exceções
except* (CustomError1, CustomError2) as e:
    print(f"Capturada uma exceção de grupo 1: {e}")
except* (CustomError3,) as e:
    print(f"Capturada uma exceção de grupo 2: {e}")

# Outra tentativa para mostrar a captura de uma exceção diferente
try:
    funcao_de_teste(3)  # Levanta CustomError3
except* (CustomError1, CustomError2) as e:
    print(f"Capturada uma exceção de grupo 1: {e}")
except* (CustomError3,) as e:
    print(f"Capturada uma exceção de grupo 2: {e}")