from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank==0:
	data = 1
	comm.send(data,dest=1)
	# ~ data = comm.recv(source=size-1source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
	data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
	print("soy {} y el dato es {}",rank,data)
else:
	data = comm.recv(source=rank-1)
	print("soy {} y el dato es {}",rank,data)
	data = data+rank
	if rank == size-1:
		comm.send(data,dest=0,tag=rank)
	else:
		comm.send(data,dest=rank+1,tag=rank)
	
	
	
# ~ mpiexec --hostfile machinefile -n 4 python3 prueba.py 
