from typing import List, Tuple, Dict, Union, Callable

# Exemplo 1: Anotações básicas com tipos primitivos
def soma(a: int, b: int) -> int:
    return a + b

# Exemplo 2: Anotação de listas e tuplas usando 'typing'
def processa_lista(valores: List[int]) -> Tuple[int, int]:
    return min(valores), max(valores)

# Exemplo 3: Anotação com dicionário e valores múltiplos
def contar_palavras(texto: str) -> Dict[str, int]:
    palavras = texto.split()
    return {palavra: palavras.count(palavra) for palavra in set(palavras)}

# Exemplo 4: Uso de Union para permitir tipos diferentes
def processa_valor(valor: Union[int, float]) -> float:
    return float(valor)

# Exemplo 5: Anotações em funções que aceitam outras funções como parâmetro
def aplicar_funcao(funcao: Callable[[int, int], int], x: int, y: int) -> int:
    return funcao(x, y)

# Exemplo 6: Classes personalizadas como anotação
class Produto:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

def mostrar_produto(produto: Produto) -> str:
    return f"Produto: {produto.nome}, Preço: R$ {produto.preco:.2f}"

# Exemplo 7: Anotações com valores padrão e sem tipo explícito
def saudacao(nome: str, saudacao: str = "Olá") -> None:
    print(f"{saudacao}, {nome}!")

# Exemplo 8: Usando anotações com funções sem retorno explícito
def funcao_sem_retorno() -> None:
    print("Esta função não retorna nada")

# Chamando as funções para testar as anotações
print(soma(5, 10))  # Output: 15
print(processa_lista([10, 20, 30]))  # Output: (10, 30)
print(contar_palavras("ola mundo mundo"))  # Output: {'ola': 1, 'mundo': 2}
print(processa_valor(5.5))  # Output: 5.5
print(aplicar_funcao(soma, 3, 7))  # Output: 10

# Criando e mostrando o produto
produto = Produto(nome="Notebook", preco=3000.0)
print(mostrar_produto(produto))  # Output: Produto: Notebook, Preço: R$ 3000.00

# Saudação
saudacao("Walter")  # Output: Olá, Walter!
funcao_sem_retorno()  # Output: Esta função não retorna nada

# Exibindo as anotações de uma função
print(soma.__annotations__)
# Output: {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

# Anotando uma função lambda com o tipo Callable
minha_lambda: Callable[[int, int], int] = lambda x, y: x + y

print(minha_lambda(10, 20))  # Output: 30

import asyncio

# Função assíncrona anotada
async def buscar_dados(url: str) -> dict:
    await asyncio.sleep(1)  # Simulando uma operação assíncrona (e.g., requisição de rede)
    return {"url": url, "dados": "dados da URL"}

# Função assíncrona com anotação de um valor de retorno do tipo list
async def processar_dados(urls: list[str]) -> list[dict]:
    resultados = []
    for url in urls:
        resultado = await buscar_dados(url)
        resultados.append(resultado)
    return resultados

# Função para rodar o exemplo
async def main():
    urls = ["https://exemplo.com", "https://exemplo2.com"]
    dados = await processar_dados(urls)
    print(dados)

# Executando o loop assíncrono
asyncio.run(main())