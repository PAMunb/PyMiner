#Testa a contagem de f-strings
f"Hello, {name}!"

#Testa a contagem de f-strings
f"Hello, {name}!"

"Just a normal string."

#Testa a detecção de comentários dentro de f-strings
f"Hello, {name  # Nome do usuário}!

# Com quebra de linha
f"""
    Hello, {name
}.
"""
# Sem quebra de linha
f"Hello, {name}!" 

#Testa a contagem de expressões complexas dentro de f-strings
f"The result is {5 * (8 + 2)}."

#Testa a detecção combinada de todos os recursos da PEP 701
name = "Alice"
age = 30

greeting = f"""
Hello, {name  # Nome do usuário
}. You are {age  # Idade do usuário
} years old. Your age in five years will be {age + 5}.
"""