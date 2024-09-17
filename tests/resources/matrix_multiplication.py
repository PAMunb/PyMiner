import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

c = a @ b
d = b @ a
e = a @ b @ a

# não é uma operação
j = a + b
i = b - a

# Multiplicação escalar
f = 2 * a
g = a * 3

# Multiplicação de matrizes
e = a @ b

