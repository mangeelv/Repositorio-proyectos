# Miguel Ángel Vallejo
'''
Librería con las principales funciones utilizadas (KB)
'''
import random
import objetoskb as ob



def crear_entorno(n:int):
    '''Crea el entorno del problema'''
    matriz = []
    for i in range(n):
        lista = [ob.Habitacion('X') for j in range(n)]
        matriz.append(lista)
    matriz[0][0] = ob.Habitacion('X') # posición incial del Capitán Willard
    matriz[0][0].capitan = 'CW'
    ocupadas = [(n,n),(0,0)]
    def definir_posicion(elemento:str):
        '''Asigna habitaciones aleatorias a los distintos elementos'''
        i = n
        j = n
        while (i,j) in ocupadas:
            i = random.randint(1,n-1)
            j = random.randint(1,n-1)
        ocupadas.append((i,j))
        matriz[i][j] = ob.Habitacion(elemento)
    elementos = ['P','P','P','M','S','CK']
    for elemento in elementos:
        definir_posicion(elemento)
    for i in range(n): # Para saber donde está cada casilla
        for j in range(n):
            matriz[i][j].posicion = (i,j)
    return matriz

def visualizar_entorno(matriz: list):
    '''Muestra por pantalla el estado del entorno con índices de posiciones'''
    # Encuentra la longitud máxima de cada columna y de los índices de fila y columna
    longitudes_columnas = [max(map(len, map(str, columna))) for columna in zip(*matriz)]
    longitud_indices = max(len(str(i)) for i in range(len(matriz)))

    # Imprime los índices de las columnas
    print(f"{'':>{longitud_indices}}  ", end="  ")
    for i in range(len(matriz[0])):
        print(f"{i:>{longitudes_columnas[i]}}  ", end="  ")
    print('\n')

    # Imprime la matriz con alineación y los índices de las filas
    for i, fila in enumerate(matriz):
        print(f"{i:>{longitud_indices}}  ", end="  ")
        for elemento, longitud in zip(fila, longitudes_columnas):
            print(f"{str(elemento):>{longitud}}  ", end="  ")
        print('\n')

def codificar_perceptos(matriz:list,n:int):
    '''Codifica los perceptos de las casillas'''
    elementos = ['P','M','S']
    contador = 0
    for elemento in elementos:
        for  i in range(n):
                for j in range(n):
                    if matriz[i][j].elemento == elemento:
                        if i+1 <= n-1:
                            matriz[i+1][j].perceptos[contador] = 1
                        if i-1 >= 0:
                            matriz[i-1][j].perceptos[contador] = 1
                        if j+1 <= n-1:
                            matriz[i][j+1].perceptos[contador] = 1
                        if j-1 >= 0:
                            matriz[i][j-1].perceptos[contador] = 1
                    if elemento == 'S' and matriz[i][j].elemento == 'S': # Si estamos en la salida también se percibe el resplandor 
                        matriz[i][j].perceptos[contador] = 1
        contador += 1
    for i in range(n):
        matriz[0][i].perceptos[3] = 1 # arriba
        matriz[n-1][i].perceptos[4] = 1 # abajo
        matriz[i][0].perceptos[5] = 1 # izquierda
        matriz[i][n-1].perceptos[6] = 1 # derecha
    return matriz

def jugar(matriz:list,capitan_willard:ob.Capitan_Willard,n:int):
    '''Define la interacción del jugador con el entorno'''
    print('''
        ---BUSCANDO AL CORONEL KURTZ---
        1.Moverse (w,s,a,d)
        2.Detonar (dt)
        3.Salir (sl)''')
    print(' ')
    matriz = capitan_willard.motor_inferencia(matriz)
    visualizar_entorno(matriz)
    while True:
        accion = input('Introduce la acción: ')
        if accion in ['w','s','a','d']:
            matriz = capitan_willard.moverse(matriz,accion)
            matriz = capitan_willard.motor_inferencia(matriz)
            visualizar_entorno(matriz) 
        elif accion == 'dt':
            matriz = capitan_willard.detonar(matriz,n)
            matriz = capitan_willard.motor_inferencia(matriz)
            visualizar_entorno(matriz)
        elif accion == 'sl':
            salir = capitan_willard.salir(matriz)
            if salir == 1:
                if capitan_willard.coronel_encontrado == 0:
                    print('Misión fallida, abandonaste al coronel')
                else:
                    print('Mision completada')
                break 
            else:
                print('No se puede salir desde esta habitación')
                matriz = capitan_willard.motor_inferencia(matriz)
                visualizar_entorno(matriz)
        i = capitan_willard.posicion[0]
        j = capitan_willard.posicion[1]
        # El capitán encuentra al coronel 
        if matriz[i][j].elemento == 'CK':
            capitan_willard.coronel_encontrado = 1
            print('Coronel Kurtz encontrado!')
        # El capitan muere
        elif matriz[i][j].elemento in ['P','M']:
            print(f'El capitan muere. Causa de muerte: {matriz[i][j].elemento}')
            break 

def obtener_adyacentes(i:int,j:int,n:int):
    adyacentes = []
    if i+1 <= n-1:
        adyacentes.append((i+1,j))
    if i-1 >= 0:
        adyacentes.append((i-1,j))
    if j+1 <= n-1:
        adyacentes.append((i,j+1))
    if j-1 >= 0:
        adyacentes.append((i,j-1))
    return adyacentes




        



    



        
       

