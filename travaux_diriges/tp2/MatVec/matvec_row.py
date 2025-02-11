# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI 
from time import time

comm = MPI.COMM_WORLD.Dup()
rank = comm.rank
size = comm.size
# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
num_row = dim//size
first_row = num_row * rank

local_A = np.array([ [(i+j+first_row)%dim+1. for j in range(dim)] for i in range(num_row) ])
print(f"local_A = {local_A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(f"u = {u}")

deb = time()
# Produit matrice-vecteur
local_v = local_A.dot(u)
print(f"local_v = {local_v}")

v = np.empty(dim,dtype=local_v.dtype)
comm.Allgather(local_v,v)
print(f"v = {v}")

fin = time()
print(f"Temps du calcul est : {fin-deb}")