# Exemplo Básico

name = "Walter"
age = 30
greeting = f"Olá, meu nome é {name} e eu tenho {age} anos."
print(greeting)  # Output: Olá, meu nome é Walter e eu tenho 30 anos.

# Expressões em F-Strings

x = 5
y = 10
result = f"A soma de {x} e {y} é {x + y}."
print(result)  # Output: A soma de 5 e 10 é 15.

# Formatação de Números

pi = 3.141592653589793
formatted_pi = f"O valor de pi é aproximadamente {pi:.2f}."
print(formatted_pi)  # Output: O valor de pi é aproximadamente 3.14.

# Data e Hora

from datetime import datetime

now = datetime.now()
formatted_date = f"A data e hora atuais são: {now:%Y-%m-%d %H:%M:%S}."
print(formatted_date)  # Output: A data e hora atuais são: YYYY-MM-DD HH:MM:SS

# Substituição de Variáveis em Nomes de Campos

data = {"nome": "Walter", "idade": 30}
message = f"Nome: {data['nome']}, Idade: {data['idade']}."
print(message)  # Output: Nome: Walter, Idade: 30.

# uso de metodos

name = "walter lucas"
greeting = f"Olá, {name.title()}!"  # Chama o método title()
print(greeting)  # Output: Olá, Walter Lucas!

# F-Strings com Cálculos

a = 7
b = 3
message = f"A média entre {a} e {b} é {(a + b) / 2}."
print(message)  # Output: A média entre 7 e 3 é 5.0.

# Formatação de Percentuais

value = 0.85
percentage = f"O valor em porcentagem é {value:.2%}."
print(percentage)  # Output: O valor em porcentagem é 85.00%.


value = 0.85
percentage = f"{value:.2%}"

# F-Strings e Escapamento

value = 42
message = f"{{valor}} é uma chave literal e não será formatada: {value}."
print(message)  # Output: {valor} é uma chave literal e não será formatada: 42.

# F-Strings com Listas

fruits = ["maçã", "banana", "laranja"]
message = f"Minhas frutas favoritas são: {', '.join(fruits)}."
print(message)  # Output: Minhas frutas favoritas são: maçã, banana, laranja.

# Exemplo de f-string com comentário no meio da interpolação
nome = "João"
idade = 30

# F-string com comentário dentro
saudacao = f"Olá, {nome}!"  # Este é o nome da pessoa
mensagem = f"Você tem {idade} anos."  # Idade de João

# F-string com quebras de linha
mensagem_completa = f""" 
Olá, {nome}.
Você tem {idade} anos.
Espero que tenha um ótimo dia!
"""  # Fim da mensagem

print(saudacao)
print(mensagem)
print(mensagem_completa)
