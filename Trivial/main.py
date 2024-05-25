if __name__ == "__main__":
    import funciones as f
    import objetos as ob
    import requests
    # Obtenemos las preguntas
    lista_diccionarios = []
    #---------------------------ENTRETENIMIENTO---------------------------
    link_entretenimiento = 'https://opentdb.com/api.php?amount=10&category=11'
    st_entretenimiento = requests.get(link_entretenimiento)
    json_dict_entretenimiento = st_entretenimiento.json()
    lista_diccionarios.append(json_dict_entretenimiento)
    #---------------------------HISTORIA---------------------------
    link_historia = 'https://opentdb.com/api.php?amount=10&category=23'
    st_historia = requests.get(link_historia)
    json_dict_historia = st_historia.json()
    lista_diccionarios.append(json_dict_historia)
    #---------------------------ARTE---------------------------
    link_arte = 'https://opentdb.com/api.php?amount=10&category=25'
    st_arte = requests.get(link_arte)
    json_dict_arte = st_arte.json()
    lista_diccionarios.append(json_dict_arte)
    #---------------------------GEOGRAFÍA---------------------------
    link_geografia = 'https://opentdb.com/api.php?amount=10&category=22'
    st_geografia = requests.get(link_geografia)
    json_dict_geografia = st_geografia.json()
    lista_diccionarios.append(json_dict_geografia)
    #---------------------------DEPORTES---------------------------
    link_deportes = 'https://opentdb.com/api.php?amount=10&category=21'
    st_deportes = requests.get(link_deportes)
    json_dict_deportes = st_deportes.json()
    lista_diccionarios.append(json_dict_deportes)
    #---------------------------CIENCIA---------------------------
    link_ciencia = 'https://opentdb.com/api.php?amount=10&category=17'
    st_ciencia = requests.get(link_ciencia)
    json_dict_ciencia = st_ciencia.json()
    lista_diccionarios.append(json_dict_ciencia)
    # Creamos el tablero
    tablero = ob.Tablero() # se inicializa el tablero vacío
    tablero = f.crear_tablero(tablero,lista_diccionarios)
    # tablero.mostrar_tablero()
    lista_jugadores = f.inicializar_jugadores(tablero)
    jugador1 = lista_jugadores[0]
    jugador2 = lista_jugadores[1]
    jugador3= lista_jugadores[2]
    jugador4 = lista_jugadores[3]
    print("BIENVENIDO A TRIVIAL")

print("Jugador 1: ",jugador1.nombre)
print("Jugador 2: ",jugador2.nombre)
print("Jugador 3: ",jugador3.nombre)
print("Jugador 4: ",jugador4.nombre)
jugadores = lista_jugadores

print("Se lanzan los dados, el jugador con el numero mas alto comienza, en caso de empate se vuelve a lanzar")
maximo = 0
for h in range(len(jugadores)):
    movimientos = f.dados()
    print("El jugador ",jugadores[h].nombre," sacó ",movimientos,".")
    if movimientos > maximo:
        maximo = movimientos
        ganador = h
        j = h



print(f'El ganador es {jugadores[ganador].nombre} ({maximo}) y comienza el juego seguido de {jugadores[ganador+1].nombre}')
print("Comienza el juego")



while((jugador1.ganar or jugador2.ganar or jugador3.ganar or jugador4.ganar) != True):
    
    if((jugador1.ganar or jugador2.ganar or jugador3.ganar or jugador4.ganar) != True):
        f.turno_jugador(jugadores[ganador],ganador + 1)
        if ganador ==3:
            ganador = -1
    
    if((jugador1.ganar or jugador2.ganar or jugador3.ganar or jugador4.ganar) != True):
        f.turno_jugador(jugadores[ganador+1],ganador + 2)
        if ganador + 1 == 3:
            ganador = -2
    
    if((jugador1.ganar or jugador2.ganar or jugador3.ganar or jugador4.ganar) != True):
        f.turno_jugador(jugadores[ganador+2],ganador + 3)
        if ganador + 2  ==3:
            ganador = -3
    
    if((jugador1.ganar or jugador2.ganar or jugador3.ganar or jugador4.ganar) != True):
        f.turno_jugador(jugadores[ganador+3],ganador + 4)
    
    ganador =  j