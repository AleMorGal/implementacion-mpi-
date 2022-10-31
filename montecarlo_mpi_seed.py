# Simulacion Montecarlo que obtinene las probabilidades de obtener cada una de las posibles 
# combinaciones en un juego de Póker con una mano de 5 cartas

# Ejecutar con mpiexec -n 8 python montecarlo_mpi.py
#  mpiexec --hostfile <hostfile> python montecarlo_mpi.py

import random
import collections  
from mpi4py import MPI

#El palo es cualquiera de las categorías en que se dividen las cartas de una baraja
PALOS = ['Espadas','Diamantes','Corazonez','Treboles']
#Valores que puede tomar cada tipo de carta (el As = 1, Jack = 11, la Reina = 12 y el Rey = 13)
VALORES = [1,2,3,4,5,6,7,8,9,10,11,12,13]

#Funcion que crea la baraja (Crea la baraja de 52 cartas (13 de cada tipo))
def crear_baraja():
    baraja = []
    for palo in PALOS:
        for valor in VALORES:
            baraja.append((palo,valor))
            
    return baraja

#Funcion la mano de cada jugador con 5 cartas (Devuelve arreglo de N manos con 5 cartas cada mano)
def repartir_cartas(baraja, numJugadores, semilla):
    #Eligira (numJugadores * 5) cartas aleatorias
    random.seed(semilla)
    cartasRepartidas = random.sample(baraja, numJugadores*5)
    #Jugador actual de de numJugadores
    jugador = 0
    #Arreglo que guarda las manos de cada jugador
    manos = []
    
    while jugador <= numJugadores -1:
        #Le reparte 5 cartas a cada jugador
        manos.append([cartasRepartidas[jugador],cartasRepartidas[jugador + numJugadores -1],
                      cartasRepartidas[jugador + numJugadores*2 -1], cartasRepartidas[jugador + numJugadores*3 -1],
                      cartasRepartidas[jugador + numJugadores*4 -1]])
        
        jugador += 1
    
    return manos

#Para encontrar pares (2 cartas del mismo valor)
def pares(mano):
    # La mano tiene una estructura [palo][valor], carta quedaria como [numero de carta][palo/valor 0/1]
    # El 1 significa que se revisa el valor de la carta
    cartas = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    pares = 0
    
    #counter cuenta las veces que se repite el valor de una carta en la mano y lo guarda en una coleccion 
    # dict jala el valor de cada uno de los items en la coleccion 
    contador = dict(collections.Counter(cartas))
    
    for valor in contador.values() :
        if valor == 2:
            pares += 1
            
    if pares == 1:
        resultado_de_mano = 'Un par'
    elif pares == 2:
        resultado_de_mano = 'Dos pares'
    else:
        resultado_de_mano = None
    
    return resultado_de_mano


#Para encontrar tercias (3 cartas del mismo valor)
def tercia(mano):
    cartas = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    
    contador = dict(collections.Counter(cartas))
    for valor in contador.values():
        if valor == 3:
            resultado_de_mano = 'Tercia'
            return resultado_de_mano
    
    return None


#Para encontrar color (5 cartas del mismo palo(tipo))
def flush(mano):
    # El 0 significa que se revisa el palo (tipo) de la carta
    palos = [mano[0][0], mano[1] [0], mano[2][0], mano[3][0], mano[4][0]]
    
    contador_palos = dict(collections.Counter(palos))
    for palo in contador_palos.values():
        if palo == 5:
            resultado_de_mano = 'Color'
            return resultado_de_mano
        
    return None


#Para encontrar escaleras (es una combinación de cinco cartas consecutivas)
def straight(mano) :
    valores = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    #.sort ordena los valores de menor a mayor
    valores.sort()
    i = valores[0]
    
    if valores [0] == i and valores [1] == i+1 and valores[2] == i+2 and valores [3] == i+3 and valores[4] == i+4:
        resultado_de_mano = 'Escalera'
        return resultado_de_mano
    
    return None

#Para encontrar Full House (combinación de tres cartas del mismo valor más una pareja distinta)
def full_house(mano):
    cartas = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    tercia = 0
    par = 0
    
    #counter cuenta las veces que se repite el valor de una carta en la mano y lo guarda en una coleccion 
    # dict ajala el valor de cada uno de los items en la coleccion 
    contador = dict(collections.Counter(cartas))
    for valor in contador.values():
        if valor == 3:
            tercia = 1
        if valor == 2:
            par += 1
        
    if tercia == 1 and par == 1:
        resultado_de_mano = 'Full house'
        return resultado_de_mano
        
    return None

#Para encontrar Pokers (cuatro cartas del mismo valor)
def poker(mano):
    cartas = [mano [0] [1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]

    contador = dict(collections.Counter(cartas))
    for valor in contador.values ():
        if valor == 4:
            resultado_de_mano = 'Poker'
            return resultado_de_mano
    
    return None

#Para encontrar Escalera de Color  (cinco cartas en orden numérico, todas del mismo palo)
def straight_flush(mano) :
    palos = [mano[0][0], mano[1][0], mano[2][0], mano[3][0], mano[4][0]]
    valores = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    #Ordena los valores de menor a mayor
    valores.sort()
    
    mismo_palo = False
    corrida = False
    
    #Verifica que todas las cartas sean del mismo tipo
    contador_palos = dict(collections.Counter(palos))
    for palo in contador_palos.values ():
        if palo == 5:
            mismo_palo = True
    
    #Toma el valor mas pequenio
    i = valores [0]
    
    if valores [0] == i and valores [1] == i+1 and valores [2] == i+2 and valores[3] == i+3 and valores [4] == i+4:
        resultado_de_mano = 'Escalera'
        corrida = True
    
    if mismo_palo == True and corrida == True:
        resultado_de_mano = 'Escalera de color'
        return resultado_de_mano
    
    return None


#Para encontrar la flor imperial  (las cinco cartas de mayor valor consecutivas (el As = 1, el Jack = 11, la Reina = 12, el Rey = 13 y el 10) y deben ser del mismo palo (tipo)
def royal_flush(mano):
    palos = [mano[0][0], mano[1][0], mano[2][0], mano[3][0], mano[4][0]]
    valores = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    #Ordena los valores de menor a mayor
    valores. sort()
    
    mismo_palo = False
    corrida_mayor = False
    
    #Revisa que sean del mismo tipo las 5 cartas
    contador_palos = dict(collections.Counter(palos))
    for valor in contador_palos.values():
        if valor == 5:
            mismo_palo = True
    
    #(el As = 1, el 10, el Jack = 11, la Reina = 12 y el Rey = 13)
    if valores[0] == 1 and valores[1] == 10 and valores [2] == 11 and valores [3] == 12 and valores[4] == 13:
        corrida_mayor = True
    
    if mismo_palo == True and corrida_mayor == True:
        resultado_de_mano = 'Flor imperial'
        return resultado_de_mano
    
    return None

#Simulacion del juego
def juego(baraja, numero_de_jugadores, semilla) :
    # Devuelve arreglo N manos de 5 cartas cada mano
    manos = repartir_cartas(baraja, numero_de_jugadores, semilla)
    
    resultados = []
    
    # Por cada jugador
    for jugador in range(numero_de_jugadores):
        
        #Guardara en el arreglo de resultados, si encontro o no la combinacion de cartas
        
        #El primer resultado se guarda si o si debido a que si no encuentra ninguna combinacion el arreglo
        # estaria vacio y habria problemas con el return
        resultados.append(pares(manos[jugador]))
        
        if tercia(manos[jugador]) != None:
            resultados[jugador] = tercia(manos[jugador])
            
        if straight(manos[jugador]) != None:
            resultados[jugador] = straight(manos[jugador])
            
        if flush(manos[jugador]) != None:
            resultados[jugador] = flush(manos[jugador])
            
        if full_house(manos[jugador ]) != None:
            resultados[jugador] = full_house(manos[jugador])
            
        if poker(manos[jugador]) != None:
            resultados[jugador] = poker(manos[jugador])
            
        if straight_flush(manos[jugador]) != None:
            resultados[jugador] = straight_flush(manos[jugador])
            
        if royal_flush(manos [jugador]) != None:
            resultados[jugador] = royal_flush(manos[jugador])
    
    return resultados


#Simulacion Montecarlo
def simulacion_montecarlo(numero_de_jugadores, numero_de_simulaciones, rank):
    baraja = crear_baraja()
    simulacion_actual = 0
    
    un_par = 0
    dos_pares = 0
    tercia = 0
    color = 0
    escalera = 0
    full_house = 0
    poker = 0
    escalera_de_color = 0
    flor_imperial = 0
    
    # Repetira el experimento la cantidad de veces que reciba en (numero_de_simulaciones)
    while numero_de_simulaciones > simulacion_actual:
        
        semilla = (rank*numero_de_simulaciones) + simulacion_actual
        resultados = juego(baraja, numero_de_jugadores, semilla)
        jugador = 0

        #Revisa los resultados de cada jugador
        for jugador in range(numero_de_jugadores):
            if resultados[jugador] == 'Un par':
                un_par += 1
            if resultados[jugador] == 'Dos pares':
                dos_pares += 1
            if resultados[jugador] == 'Tercia':
                tercia += 1
            if resultados[jugador] == 'Color':
                color += 1
            if resultados[jugador] == 'Escalera':
                escalera += 1
            if resultados[jugador] == 'Full house':
                full_house += 1
            if resultados[jugador] == 'Poker':
                poker += 1
            if resultados[jugador] == 'Escalera de color':
                escalera_de_color += 1
            if resultados[jugador] == 'Flor imperial':
                flor_imperial + 1
            
        simulacion_actual += 1
        
    #Cantidad de veces que se obtuvieron las combinaciones en las (numero_de_simulaciones) veces que se ejecuto el experimento
    combinaciones_obtenidad = [un_par, dos_pares, tercia, color, escalera, full_house, 
                            poker, escalera_de_color, flor_imperial]
    
    return combinaciones_obtenidad


#-----------------------------------------------------------------
#           FUNCION PRINCIPAL QUE HACE USO DE MPI
#----------------------------------------------------------------    
if __name__ == "__main__":
    #comm es nuestro objeto comunicador
    comm = MPI.COMM_WORLD
    # Get_size devuelve el nnumero total de procesos que hay
    size = comm.Get_size()
    # Get_rank devuelve el numero identificador del proceso
    rank = comm.Get_rank()
    
    # numero de judores
    numjugadores = 4
    # Cantidad de veces que realizara el experimento cada proceso
    simulaciones = 10000
    # Arreglo que almacenara los respuestas finales
    resultados_finales = [0,0,0,0,0,0,0,0,0]
    # Total de combinaciones que se encontraron en todas las simulaciones
    combinaciones = 0
    # Arreglo que guarda cual es la probabilidad de obtener las combinaciones en base a
    # los resultado obtenidos en las simulaciones
    probabilidades = [0,0,0,0,0,0,0,0,0]
    
    # El proceso 0 sera el encargado de recibir los resultados de los demas procesos
    if rank == 0:
        for i in range(size-1):
            resultados_recibidos = comm.recv(source=i+1)
            # Guarda la cantidad de veces que se encontro cada combinacion
            for j in range(9):
                resultados_finales[j] = resultados_finales[j] + resultados_recibidos[j]
    # Los demas procesos realizan la simulacion y envian sus resultados a el proceso 0
    else:
        resultados = simulacion_montecarlo(numjugadores, simulaciones, rank)
        comm.send(resultados, dest=0)
     
    # El proceso 0 muestra los resultados finales
    if rank == 0:
        # Total de simulaciones realizadas por todos los procesos
        cantidad_simulaciones = simulaciones * (size-1) * numjugadores

        #Obtiene la cantidad de combinaciones totales, asi como, obtiene cual fue la probabilidad de cada posibilidad
        for j in range(9):
            combinaciones = combinaciones + resultados_finales[j]
            probabilidades[j] = resultados_finales[j] / cantidad_simulaciones
            
        
        # Muestra los resultados en pantalla
        print('\nSe obtuvieron {} combinaciones de un total de {} simulaciones\n'.format(combinaciones, cantidad_simulaciones))
        print('Un par se encontro {} veces: {}%'.format(resultados_finales[0], round(probabilidades[0]*100, 5)))
        print('Dos pares se encontro {} veces: {}%'.format(resultados_finales[1], round(probabilidades[1]*100, 5)))
        print('Tercia se encontro {} veces: {}%'.format(resultados_finales[2], round(probabilidades[2]*100, 5)))
        print('Color se encontro {} veces:  {}%'.format(resultados_finales[3], round(probabilidades[3]*100, 5)))
        print('Escalera se encontro {} veces:  {}%'.format(resultados_finales[4], round(probabilidades[4]*100, 5)))
        print('Full House se encontro {} veces:  {}%'.format(resultados_finales[5], round(probabilidades[5]*100, 5)))
        print('Poker se encontro {} veces:  {}%'.format(resultados_finales[6], round(probabilidades[6]*100, 5)))
        print('Escalera de color se encontro {} veces: {}%'.format(resultados_finales[7], round(probabilidades[7]*100, 5)))
        print('Flor Imperial {} veces: {}%'.format(resultados_finales[8], round(probabilidades[8]*100, 5)))