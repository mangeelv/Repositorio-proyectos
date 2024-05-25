import objetos as ob
import random
import time
def dados():
    dado1 = random.randint(1,6)
    dado2 = random.randint(1,6)
    movimientos = dado1 + dado2
    return movimientos
#----------------------------------------------------------------------------------------------------------------
def inicializar_jugadores(tablero:ob.Tablero):
    # Creamos los 4 jugadores
    jugador1 = ob.jugador()
    jugador2 = ob.jugador()
    jugador3 = ob.jugador()
    jugador4 = ob.jugador()
    lista_jugadores = [jugador1,jugador2,jugador3,jugador4]
    print("¡Bienvenidos as Trivial!")
    print("Introducid vuestros nombres: ")
    for i in range(4):
        lista_jugadores[i].posicion = tablero.head
        lista_jugadores[i].ganar = False
        lista_jugadores[i].ent = False
        lista_jugadores[i].hist = False
        lista_jugadores[i].art = False
        lista_jugadores[i].geo = False
        lista_jugadores[i].dep = False
        lista_jugadores[i].cien = False
        lista_jugadores[i].nombre = input(f"jugador {i+1} : ")
    return lista_jugadores
def crear_tablero(tablero:ob.Tablero,lista_diccionarios:list):
    lista_categorias = ['entretenimiento', 'historia', 'arte', 'geografia', 'deportes','ciencia']
    for i in range(6): # creamos las 6 primeras casillas
        casilla = ob.casilla() # este será el head del tablero
        casilla.preguntas = lista_diccionarios[i] # orden: E H A G D C
        casilla.fin = False 
        casilla.numero = i 
        casilla.especial = False
        casilla.queso = None
        casilla.categoria = lista_categorias[i]
        tablero.anadirnodo(casilla)
    for i in range(6):
        # creamos casilla especial
        casilla = ob.casilla()
        casilla.preguntas = lista_diccionarios[i] # orden: E H A G D C
        casilla.fin = False 
        casilla.numero = i 
        casilla.especial = True
        casilla.queso = lista_categorias[i]
        casilla.categoria = lista_categorias[i]
        tablero.anadirnodo(casilla)
        if i < 5: # este bucle acaba con la última casilla especial
            for i in range(6): # creamos las casillas intermedias
                casilla = ob.casilla()
                casilla.preguntas = lista_diccionarios[i] # orden: E H A G D C
                casilla.fin = False 
                casilla.numero = i 
                casilla.especial = False
                casilla.queso = None
                casilla.categoria = lista_categorias[i]
                tablero.anadirnodo(casilla)
    for i in range(5): # creamos las 5 antepenultimas casillas
        casilla = ob.casilla()
        casilla.preguntas = lista_diccionarios[i] # orden: E H A G D C
        casilla.fin = False 
        casilla.numero = i 
        casilla.especial = False
        casilla.queso = None
        casilla.categoria = lista_categorias[i]
        tablero.anadirnodo(casilla)
    casilla = ob.casilla() # creamos la ultima casilla (el tail del tablero)
    casilla.preguntas = lista_diccionarios[5] # orden: E H A G D C
    casilla.fin = True 
    casilla.numero = i 
    casilla.especial = False
    casilla.queso = None
    casilla.categoria = lista_categorias[5]
    tablero.anadirnodo(casilla)
    return tablero
def turno_jugador(jugador:ob.jugador,numero_jugador:int):
    '''Cada ejecución de esta función corresponde con un turno del jugador. Se ejecuta de forma recursiva hasta que el jugador responda incorrectamente.'''
    print(f"-----Turno del jugador {numero_jugador}-----")
    casilla = jugador.posicion # Obtenemos la posicion actual del jugador
    print(f'Casilla numero {casilla.numero}')
    if casilla.especial == True:
        print(f"¡Casilla Superespecial de la categoría {casilla.queso}!")
    else:
        print(f"Categoría: {casilla.categoria}")
    n = random.randint(0,len(casilla.preguntas['results'])-1)
    pregunta = casilla.preguntas['results'][n] # seleccionamos una pregunta del diccionario, aleatoriamente
    print(pregunta['question'])
    respuesta_correcta = pregunta['correct_answer'] # obtenemos la respuesta correcta
    # print(f"RC: {respuesta_correcta}")
    n = random.randint(0,len(pregunta['incorrect_answers'])-1) # seleccionamos indice aleatorio para mostrar la respuesta correcta por pantalla, junto con las incorrectas
    for i in range(len(pregunta['incorrect_answers'])):
        if i == n:
            print(respuesta_correcta)
        print(pregunta['incorrect_answers'][i])
    respuesta_jugador = input("Introduce la respuesta: ")
    if respuesta_jugador != respuesta_correcta: # si la respuesta es incorrecta, el jugador permanece en la casilla
        print("Respuesta incorrecta")
        return # condición de salida de la recursividad
    else:
        print("¡Respuesta correcta!")
        if casilla.especial == True:
            print(f"Enhorabuena, {jugador.nombre} ganaste el queso {casilla.queso}!")
            if casilla.queso == 'entrenenimiento':
                jugador.ent = True
            elif casilla.queso == 'historia':
                jugador.hist = True
            elif casilla.queso == 'arte':
                jugador.art = True
            elif casilla.queso == 'geografia':
                jugador.geo = True
            elif casilla.queso == 'deportes':
                jugador.dep = True
            elif casilla.queso == 'ciencia':
                jugador.cien = True
        # condicion de victoria
        if jugador.ent and jugador.hist and jugador.art and jugador.geo and jugador.dep and jugador.cien:
            print(f"¡Enhorabuena {jugador.nombre}, has ganado!")
            jugador.ganar = True
            return 
        print("Tirando dados....")
        time.sleep(2) # esperamos 2 segundillos para dare emoción al asunto
        movimientos = dados() # devuelve un entero con el numero de movimientos
        movimientos = 6
        print(f"¡Has sacado un {movimientos}!")
        direccion = int(input("Introduce 1 para ir hacia delante o 0 para ir hacia atrás: "))

        if direccion == 1:
            for i in range(movimientos):
                jugador.posicion = jugador.posicion.next
        else:
            for i in range(movimientos):
                jugador.posicion = jugador.posicion.prev
        
        print(f"Avanzas a la posicion {jugador.posicion.numero}")
        turno_jugador(jugador,numero_jugador) # Usamos recursividad, el jugador repite turno 




