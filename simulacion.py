from mpi4py import MPI
import random
import collections

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

palos = ['Espadas','Trebol','Corazon','Diamante']
valores = ['As',2,3,4,5,6,7,8,9,10,'Joto','Reina','Rey']

def pares(mano):
	repetidas = 0
	for i in range(len(mano)):
		carta = mano[i][0]
		for j in range(i+1,len(mano)):
			if str(carta) == str(mano[j][0]):
				repetidas += 1
				
	return repetidas
	
def escaleraReal(mano):
	if (mano[0][1] == mano[1][1] and mano[0][0] == 'As'):
		if (mano[1][1] == mano[2][1] and mano[1][0] == 'Rey'):
			if (mano[2][1] == mano[3][1] and mano[2][0] == 'Reina'):
				if (mano[3][1] == mano[4][1] and mano[3][0] == 'Joto'):
					if (mano[4][0] == 10):
						return 1
				
			
	return 0
		
def escaleraColor(mano):
	numMasAlto = mano[0][0]
	pos = valores.index(numMasAlto)
	if pos > 4:
		if (mano[0][1] == mano[1][1] and mano[1][0] == valores[pos-1] ):
			if (mano[1][1] == mano[2][1] and mano[2][0] == valores[pos-2]):
				if (mano[2][1] == mano[3][1] and mano[3][0] == valores[pos-3]):
					if (mano[3][1] == mano[4][1] and mano[4][0] == valores[pos-4]):
						# ~ if (mano[4][0]-1 == valores[pos]-5):
						return 1
				
			
	return 0
	
def poker(mano):
	numRepetidas = 0
	arrayAux =[]
	for i in range(len(mano)):
		arrayAux.append(mano[i][0])
		
	for i in range(len(arrayAux)):
		if arrayAux.count(arrayAux[i]) > numRepetidas:
			numRepetidas = arrayAux.count(arrayAux[i])
			
	
	if numRepetidas == 4:
		return 1
	else:
		return 0
		
def full(mano):
	numRepetidasMayor = 0
	numRepetidasMenor = 0
	arrayAux =[]
	for i in range(len(mano)):
		arrayAux.append(mano[i][0])
		
	for i in range(len(arrayAux)):
		countActual = arrayAux.count(arrayAux[i])
		if countActual > numRepetidasMayor:
			numRepetidasMenor = numRepetidasMayor
			numRepetidasMayor = arrayAux.count(arrayAux[i])
		elif countActual < numRepetidasMayor:
			numRepetidasMenor = arrayAux.count(arrayAux[i])
	
	if numRepetidasMayor == 3 and numRepetidasMenor == 2:
		return 1
	else:
		return 0
	
def color(mano):
	if (mano[0][1] == mano[1][1] ):
		if (mano[1][1] == mano[2][1] ):
			if (mano[2][1] == mano[3][1]):
				if (mano[3][1] == mano[4][1]):
					return 1
				
			
	return 0

def escalera(mano):
	numMasAlto = mano[0][0]
	pos = valores.index(numMasAlto)
	if pos > 4:
		if (mano[1][0] == valores[pos-1] ):
			if (mano[2][0] == valores[pos-2]):
				if ( mano[3][0] == valores[pos-3]):
					if (mano[4][0] == valores[pos-4]):
						# ~ if (mano[4][0]-1 == valores[pos]-5):
						return 1
				
			
	return 0
	
def trio(mano):
	numRepetidas = 0
	arrayAux =[]
	for i in range(len(mano)):
		arrayAux.append(mano[i][0])
		
	for i in range(len(arrayAux)):
		if arrayAux.count(arrayAux[i]) > numRepetidas:
			numRepetidas = arrayAux.count(arrayAux[i])
			
	
	if numRepetidas == 3:
		return 1
	else:
		return 0

def doblePareja(mano):
	numRepetidas1 = 0
	numRepetidas2 = 0
	valor = 0
	arrayAux =[]
	for i in range(len(mano)):
		arrayAux.append(mano[i][0])
		
	for i in range(len(arrayAux)):
		countActual = arrayAux.count(arrayAux[i])
		if countActual == 2 and arrayAux[i] != valor:
			valor = arrayAux[i]
			if numRepetidas1 == 0:
				numRepetidas1 = arrayAux.count(arrayAux[i])
			else:
				numRepetidas2 = arrayAux.count(arrayAux[i])
	
	if numRepetidas1 == 2 and numRepetidas2 == 2:
		return 1
	else:
		return 0
		
	
def pareja(mano):
	numRepetidas = 0
	arrayAux =[]
	for i in range(len(mano)):
		arrayAux.append(mano[i][0])
		
	for i in range(len(arrayAux)):
		if arrayAux.count(arrayAux[i]) == 2:
			return 1
			
	
	# ~ if numRepetidas == 2:
		# ~ return 1
	# ~ else:
	return 0
		
def juego(baraja,resultados):
	# ~ resultados = [0,0,0,0,0,0,0,0,0,0]
	
	if(escaleraReal(baraja)):
		resultados[0] += 1
	elif (escaleraColor(baraja)):
		resultados[1] += 1
	elif (poker(baraja)):
		resultados[2] += 1
	elif (full(baraja)):
		resultados[3] += 1
	elif (color(baraja)):
		resultados[4] += 1
	elif (escalera(baraja)):
		resultados[5] += 1
	elif (trio(baraja)):
		resultados[6] += 1
	elif (doblePareja(baraja)):
		resultados[7] += 1
	elif (pareja(baraja)):
		resultados[8] += 1
	else:
		resultados[9] += 1
	# ~ print("soy el rank"+str(rank)+" "+str(numPares)+"-"+str(numTercia)+"-"+str(numStraight)+"-"+str(numFlush)+"-"+str(numFullHouse)+"-"+str(numPoker)+"-"+str(numRoyalFlush))
	# ~ for i in range(len(resultados)):
		# ~ print("soy el rank-"+str(rank)+" y la suma es del elemento "+str(i)+" es "+str(resultados[i]))
	return resultados

def sumaArrays(array, newArray):
	for i in range(len(array)):
		array[i] += newArray[i]
		
	return array
	
if __name__ == "__main__":
	barajaMano=[]
	resultados = [0,0,0,0,0,0,0,0,0,0]
	
	if rank == 0:
		for i in range(1,size):
			# ~ req = comm.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
			# ~ newResultados  = comm.recv(source=i, tag=MPI.ANY_TAG)
			req = comm.irecv(source=i, tag=MPI.ANY_TAG)
			newResultados = req.wait()
			resultados = sumaArrays(resultados,newResultados)
		
		for i in range(len(resultados)):
			print("soy el rank-"+str(rank)+" y la suma es del elemento "+str(i)+" es "+str(resultados[i]))
	else:
		
		
			# ~ barajaMano = ([9,'Espadas'],['Reina','Espadas'],['Reina','Espadas'],[9,'Trebol'],[8,'Espadas'])
		

		for i in range(5):
			barajaMano = []
			for i in range(5):
				barajaMano.append( [random.choice(valores),random.choice(palos)]) 
				
			resultados = juego(barajaMano,resultados)
			# ~ comm.send(resultados,dest=0,tag=rank)
			req = comm.isend(resultados,dest=0,tag=rank)
			req.wait()

		for i in range(len(resultados)):
			print("soy el rank-"+str(rank)+" y la suma es del elemento "+str(i)+" es "+str(resultados[i]))



