# Miguel Ángel Vallejo
'''
Librería con las principales funciones utilizadas (BY)
'''
import random
import objetosby as ob


def crear_entorno(n:int):
    '''Crea el entorno del problema'''
    matriz = []
    for i in range(n):
        lista = [ob.Habitacion([]) for j in range(n)]
        matriz.append(lista)
    matriz[0][0] = ob.Habitacion([]) # posición incial del Capitán Willard
    matriz[0][0].capitan = 'CW'
    ocupadas = [(n,n),(0,0)]
    def definir_posicion(elemento:str):
        '''Asigna habitaciones aleatorias a los distintos elementos'''
        i = n
        j = n
        if elemento in ['F','P','D']:
            i = random.randint(1,5)
            j = random.randint(1,5)
            ocupadas.append((i,j))
            matriz[i][j].elementos.append(elemento)
        else:
            while (i,j) in ocupadas:
                i = random.randint(1,n-1)
                j = random.randint(1,n-1)
            # ocupadas.append((i,j))
            matriz[i][j].elementos.append(elemento)
    elementos = ['F','P','D','M','S','CK']
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
    elementos = ['F','P','D','M','S']
    contador = 0
    for elemento in elementos:
        for  i in range(n):
                for j in range(n):
                    for elemento_en_matriz in matriz[i][j].elementos:
                        if elemento_en_matriz == elemento:
                            if i+1 <= n-1:
                                matriz[i+1][j].perceptos[contador] = 1
                            if i-1 >= 0:
                                matriz[i-1][j].perceptos[contador] = 1
                            if j+1 <= n-1:
                                matriz[i][j+1].perceptos[contador] = 1
                            if j-1 >= 0:
                                matriz[i][j-1].perceptos[contador] = 1
                            matriz[i][j].perceptos[contador] = 1 # El estímulo también está en la celda del elemento 
                        if elemento == 'S' and  'S' in  matriz[i][j].elementos: # Si estamos en la salida también se percibe el resplandor 
                            matriz[i][j].perceptos[contador] = 1
                        
                  
        contador += 1
    for i in range(n):
        matriz[0][i].perceptos[5] = 1 # arriba
        matriz[n-1][i].perceptos[6] = 1 # abajo
        matriz[i][0].perceptos[7] = 1 # izquierda
        matriz[i][n-1].perceptos[8] = 1 # derecha
    return matriz


def jugar(matriz:list,capitan_willard,n:int):
        print('''
        ---BUSCANDO AL CORONEL KURTZ---
        1.Moverse (w,s,a,d)
        2.Disparar dardo (dd)
        3.Salir (sl)''')
        capitan_willard.mapas_probabilidad(matriz)
        visualizar_entorno(matriz)
        while True:
    
            accion = input('Introduce la acción: ')
            if accion in ['w','s','a','d']:
                matriz = capitan_willard.moverse(matriz,accion)
                capitan_willard.mapas_probabilidad(matriz)
                visualizar_entorno(matriz) 
            elif accion == 'dd':
                direccion = ''
                while direccion not in ['w','s','a','d']:
                    direccion = input('Dirección del disparo (w,s,a,d): ')
                    if direccion not in ['w','s','a','d']:
                        print('Selecciona una dirección válida')
                matriz =  capitan_willard.disparar_dardo(matriz,direccion,n)
                capitan_willard.mapas_probabilidad(matriz)
                visualizar_entorno(matriz) 

            elif accion == 'br':
                break
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
                    capitan_willard.mapas_probabilidad(matriz)
                    visualizar_entorno(matriz)
            i = capitan_willard.posicion[0]
            j = capitan_willard.posicion[1]
            muerte = False
            for elemento in matriz[i][j].elementos: # El capitán encuentra al coronel 
                if elemento == 'CK':
                    capitan_willard.coronel_encontrado = 1
                    print('Coronel Kurtz encontrado!')
                elif elemento in ['F','P','D','M']: # El capitan muere
                    print(f'El capitan muere. Causa de muerte: {elemento}')
                    muerte = True
            if muerte:
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

                
