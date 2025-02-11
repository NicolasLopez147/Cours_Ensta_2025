from mpi4py import MPI
import numpy as np

def bucket_sort(arr):
    """ Algoritmo de Bucket Sort en un solo proceso """
    if len(arr) == 0:
        return arr

    num_buckets = len(arr) // 10 + 1  # Definir número de cubetas
    buckets = [[] for _ in range(num_buckets)]

    # Distribuir los números en los buckets
    min_val, max_val = min(arr), max(arr)
    range_val = max_val - min_val + 1e-6  # Evitar divisiones por cero
    for num in arr:
        index = int((num - min_val) / range_val * (num_buckets - 1))
        buckets[index].append(num)

    # Ordenar cada bucket individualmente (podría usarse otro algoritmo)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))

    return sorted_arr


# Inicializar MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parámetros del Bucket Sort
N = 100  # Tamaño total del array a ordenar
data = None  # Datos iniciales (solo en el proceso 0)

if rank == 0:
    # Proceso 0 genera un array de números aleatorios entre 0 y 1000
    data = np.random.randint(0, 1000, size=N)
    print(f"Array inicial: {data}")

# Dividir el array entre los procesos (Scatter)
chunk_size = N // size
local_data = np.zeros(chunk_size, dtype=int)
comm.Scatter(data, local_data, root=0)

# Cada proceso ordena su parte del array
local_sorted = bucket_sort(local_data.tolist())

# Recolectar los datos ordenados en el proceso 0 (Gather)
sorted_data = None
if rank == 0:
    sorted_data = np.empty(N, dtype=int)
comm.Gather(np.array(local_sorted, dtype=int), sorted_data, root=0)

# Proceso 0 combina los datos ordenados
if rank == 0:
    sorted_final = bucket_sort(sorted_data.tolist())  # Orden final tras Gather
    print(f"Array ordenado: {sorted_final}")
