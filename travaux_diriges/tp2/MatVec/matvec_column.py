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
num_col = dim//size
first_col = num_col * rank

local_A = np.array([ [(i+j+first_col)%dim+1. for j in range(num_col)] for i in range(dim) ])
print(f"local_A = {local_A}")

# Initialisation du vecteur u
local_u = np.array([i+1. + first_col for i in range(num_col)])
print(f"local_u = {local_u}")


deb = time()
# Produit matrice-vecteur
local_v = local_A.dot(local_u)
print(f"local_v = {local_v}")

v = np.empty(dim,dtype=local_v.dtype)
comm.Allreduce(local_v,v)
print(f"v = {v}")

fin = time()
print(f"Temps du calcul est : {fin-deb}")
# Normal 0.0004932880401611328
#Column 0.0010089874267578125
#Row 0.001424551010131836