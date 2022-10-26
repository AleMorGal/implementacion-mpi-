from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def pares(mano):
	repetidas = 0
	for i in range(len(mano)):
		carta = mano[i][0]
		for j in range(i+1,len(mano)):
			if str(carta) == str(mano[j][0]):
				repetidas += 1
				
	return repetidas
	
def juego(baraja):
	resultados = []
	
	numPares = pares(baraja)
	# ~ numTercia = tercia(baraja)
	# ~ numStraight = straight(baraja)
	# ~ numFlush = flush(baraja)
	# ~ numFullHouse = fullHouse(baraja)
	# ~ numPoker = poker(baraja)
	# ~ numRoyalFlush = royal_flush(baraja)
	# ~ print("soy el rank"+str(rank)+" "+str(numPares)+"-"+str(numTercia)+"-"+str(numStraight)+"-"+str(numFlush)+"-"+str(numFullHouse)+"-"+str(numPoker)+"-"+str(numRoyalFlush))
	print("soy el rank"+str(rank)+" "+str(numPares))
	

palos = ['Espadas','Trebol','Corazon','Diamante']
valores = [1,2,3,4,5,6,7,8,9,10,'Joto','Reina','Rey']
barajaMano=[]

for i in range(5):
	barajaMano.append( [random.choice(valores),random.choice(palos)]) 
	

for i in range(5):
	print("soy el rank"+str(rank)+" "+str(barajaMano[i][0])+"-"+barajaMano[i][1])

juego(barajaMano)



