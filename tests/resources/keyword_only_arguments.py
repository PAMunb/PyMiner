# Exemplo 1: Usando keyword-only arguments com um argumento obrigatório
def calcular_area_com_desconto(largura, altura, *, desconto):
    area = largura * altura
    area_com_desconto = area - (area * desconto)
    return area_com_desconto

# Aqui você pode passar largura e altura como posicionais, mas desconto precisa ser nomeado
print("Área com desconto:", calcular_area_com_desconto(10, 5, desconto=0.1))

# Exemplo 2: Keyword-only argument com um valor padrão
def saudacao(nome, *, mensagem="Olá"):
    return f"{mensagem}, {nome}!"

# Pode-se fornecer ou não o argumento keyword-only, já que ele tem um valor padrão
print(saudacao("Ana"))  # Usa o valor padrão de mensagem
print(saudacao("Ana", mensagem="Bem-vinda"))  # Sobrescreve o valor padrão

# Exemplo 3: Todos os argumentos como keyword-only
def info_pessoa(*, nome, idade):
    return f"Nome: {nome}, Idade: {idade}"

# Aqui, os dois argumentos precisam ser passados como palavras-chave
print(info_pessoa(nome="Carlos", idade=30))

# Exemplo 4: Misturando argumentos posicionais e keyword-only
def resumo_viagem(partida, destino, *, meio_transporte="carro"):
    return f"De {partida} para {destino} de {meio_transporte}"

# Argumentos posicionais para partida e destino, e keyword-only para meio_transporte
print(resumo_viagem("São Paulo", "Rio de Janeiro", meio_transporte="avião"))
print(resumo_viagem("São Paulo", "Rio de Janeiro"))  # Usa o valor padrão

# Exemplo 5: Usando keyword-only para evitar ambiguidades
def dividir(dividendo, divisor, *, preciso=False):
    if preciso:
        return dividendo / divisor
    else:
        return dividendo // divisor

# Aqui, "preciso" precisa ser nomeado
print(dividir(10, 3, preciso=True))  # Divisão com precisão (float)
print(dividir(10, 3))  # Divisão inteira (floor division)

# Exemplo 6: Argumentos variáveis antes de keyword-only
def somar_tudo(*valores, multiplicador=1):
    return sum(valores) * multiplicador

# Passar vários valores posicionais e um argumento keyword-only
print(somar_tudo(1, 2, 3, 4, multiplicador=2))  # Soma os valores e multiplica por 2
print(somar_tudo(5, 5, 5))  # Soma os valores e multiplica pelo valor padrão de multiplicador (1)
