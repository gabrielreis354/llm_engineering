import random

# Generate a random integer between 1 and 100
random_number = random.randint(1, 100)

# JOGO DO MARCIANO
def marciano():
  count = 0
  print("Bem-vindo ao Jogo do Marciano!")
  print("Tem um marciano escondido nas arvores, você precisa encontrar-o e matá-lo.")
  print("Exitem 100 arvores e voce tem somente 5 tiros")

  while count < 5:
      arvore = int(input("Selecione a arvore (1-100): "))
      if arvore == random_number:
          print("Você encontrou o marciano!")
          break
      elif arvore > random_number:
          print("O marciano está mais para a esquerda.")
      else:
          print("O marciano está mais para a direita.")
      count += 1
  if count == 5:
      print("Você não conseguiu encontrar o marciano.")
      print(f"O marciano estava na árvore {random_number}.")

marciano()