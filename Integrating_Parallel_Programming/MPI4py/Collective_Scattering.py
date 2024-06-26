# Scattering Python objects:
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [(i+1)**2 for i in range(size)]
else:
    data = None

# Scatter the data
data = comm.scatter(data, root=0)

# Each process prints its own data
print("Process", rank, "received data:", data)
