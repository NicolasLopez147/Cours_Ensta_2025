# Produit matrice-vecteur v = A.u
from time import time
import numpy as np

# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(f"u = {u}")


deb = time()
# Produit matrice-vecteur
v = A.dot(u)
print(f"v = {v}")
fin = time()
print(f"Temps du calcul est : {fin-deb}")