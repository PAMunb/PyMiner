
"""Teste positivo: uma única f-string"""
frase = f"Olá, {nome}!"
        
"""Teste positivo: múltiplas f-strings"""
    
nome = "Ana"
idade = 30
frase1 = f"Nome: {nome}"
frase2 = f"Idade: {idade}"
      
"""Teste positivo: f-string com expressão complexa"""
     
valor = 10
resultado = f"O dobro de {valor} é {valor * 2}"
      
"""Teste positivo: f-string com sequências de escape"""
  
nome = "João"
frase = f"Olá, \\{nome}!"
    
"""Teste positivo: f-string multiline"""
     
nome = "Maria"
frase = f"""Olá, {nome}!Como vai você?"""
   
"""Teste negativo: código sem f-strings"""
       
nome = "Carlos"
idade = 22
frase = "Meu nome é " + nome
        
"""Teste negativo: código com strings normais (sem f-strings)"""
     
nome = "Ana"
idade = 30
frase = "Meu nome é Ana"
frase2 = "Tenho 30 anos"
       
"""Teste negativo: uso de .format() em vez de f-string"""
        
nome = "Ana"
idade = 30
frase = "Nome: {}".format(nome)
frase2 = "Idade: {}".format(idade)
     
"""Teste negativo: strings concatenadas com +"""
   
nome = "Pedro"
idade = 25
frase = "Meu nome é " + nome + " e tenho " + str(idade) + " anos."
      
"""Teste negativo: uso de % para formatação"""

nome = "Ana"
idade = 30
frase = "Nome: %s" % nome
frase2 = "Idade: %d" % idade
       