from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD.Dup()
rank = comm.rank
size = comm.size
number_data = 10000000
start = time.time()

np.random.seed(rank)
local_data = np.random.rand(number_data) * 1000  
local_data.sort()  
all_data = comm.gather(local_data, root=0)

if rank == 0:
    all_data = np.concatenate(all_data)
    quantiles = np.quantile(all_data, np.linspace(0, 1, size + 1))
    print(f"Buckets limits: {quantiles}")
else:
    quantiles = None

quantiles = comm.bcast(quantiles, root=0)
send_counts = np.zeros(size, dtype=int)
send_data = [[] for _ in range(size)]

for data in local_data:
    for i in range(size):
        if quantiles[i] <= data < quantiles[i + 1] or (i == size - 1 and data == quantiles[i + 1]):
            send_data[i].append(data)
            send_counts[i] += 1
            break

send_data = [np.array(d, dtype=np.float64) for d in send_data]
send_counts = np.array(send_counts, dtype=int)
recv_counts = np.zeros(size, dtype=int)
comm.Alltoall(send_counts, recv_counts)
send_displs = np.insert(np.cumsum(send_counts[:-1]), 0, 0)
recv_displs = np.insert(np.cumsum(recv_counts[:-1]), 0, 0)
send_buffer = np.concatenate(send_data) if send_data else np.array([], dtype=np.float64)
recv_buffer = np.empty(sum(recv_counts), dtype=np.float64)
comm.Alltoallv([send_buffer, send_counts, send_displs, MPI.DOUBLE],
               [recv_buffer, recv_counts, recv_displs, MPI.DOUBLE])

recv_buffer.sort()
end = time.time()

print(f"Rank {rank} completed in {end-start:.6f} seconds")

sorted_data = comm.gather(recv_buffer, root=0)
if rank == 0:
    sorted_data = np.concatenate(sorted_data)
    print(f"Sorted Data (size {len(sorted_data)}): {sorted_data}")
