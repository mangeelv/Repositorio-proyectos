# Miguel Ángel Vallejo
'''
Librería en la que se definen objetos (KB)
'''



import funcioneskb as f 

class Habitacion(): # Esta será nuestra clase 'estado'
    def __init__(self,elemento:str):
        self.capitan = 'X'
        self.inferido = '?'
        self.elemento = elemento
        self.perceptos = [0,0,0,0,0,0,0,0] #brisa olor resplandor arriba abajo izquierda derecha grito
        self.posicion = None
    def __str__(self):
        return f'{self.capitan};{self.inferido}'
    
 
class Capitan_Willard(): # Este será nuestro agente 'KB'
    def __init__(self):
        self.posicion = [0,0]
        self.granada = 1
        self.coronel_encontrado = 0 
        self.perceptos_anteriores = {} # diccionario posicion:percepto
        self.celdas_seguras = []
        self.precipicios = []
        self.monstruo = []
        self.monstruo_vivo = 1
        self.salida = []
        self.n = 6
    
    def moverse(self,matriz:list,accion:str):
        '''Implementación de los movimientos del agente en el entorno'''
        if accion == 'w' and matriz[self.posicion[0]][self.posicion[1]].perceptos[3] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[0] -= 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 's' and matriz[self.posicion[0]][self.posicion[1]].perceptos[4] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[0] += 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 'a' and matriz[self.posicion[0]][self.posicion[1]].perceptos[5] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[1] -= 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 'd' and matriz[self.posicion[0]][self.posicion[1]].perceptos[6] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[1] += 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        else:
            print('Hay una pared, prueba otra cosa')
        return matriz
    
    def detonar(self,matriz:list,n:int):
        '''Implementación de la acción detonar'''
        if self.granada == 1:
            i = self.posicion[0]
            j = self.posicion[1]
            print('Granada detonada')
            if i+1 <= n-1 and matriz[i+1][j].elemento == 'M':
                matriz[i+1][j].elemento = 'X'
                matriz[i][j].perceptos[7] = 1 # Grito
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif i-1 >= 0 and matriz[i-1][j].elemento == 'M':
                matriz[i-1][j].elemento = 'X'
                matriz[i][j].perceptos[7] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif j+1 <= n-1 and matriz[i][j+1].elemento == 'M':
                matriz[i][j+1].elemento = 'X'
                matriz[i][j].perceptos[7] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif j-1 >= 0 and matriz[i][j-1].elemento == 'M':
                matriz[i][j-1].elemento = 'X'
                matriz[i][j].perceptos[7] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            else:
                print('El monstruo sigue vivo') # No hay grito
            self.granada -= 1
        else:
            print('No quedan granadas')
        return matriz
    
    def salir(self,matriz:list):
        '''Implementación de la acción salir'''
        i = self.posicion[0]
        j = self.posicion[1]
        if matriz[i][j].elemento == 'S':
            return 1
        else:
            return 0
        

    def motor_inferencia(self,matriz:list):
        '''Motor de inferencia del agente. Permite inferir posiciones de los elementos a partir de los perceptos.'''
        i = self.posicion[0]
        j = self.posicion[1]
        perceptos_anteriores = self.perceptos_anteriores
        percepto_actual = matriz[i][j].perceptos
        self.celdas_seguras = list(set(self.celdas_seguras)) # eliminamos posibles duplicados
        self.precipicios = list(set(self.precipicios))
        print('Informacion en la base de conocimientos (KB): ')
        print(f'Granada: {self.granada}')
        print(f'Coronel Kurtz encontrado: {self.coronel_encontrado}')
        print(f'Percepto actual: {percepto_actual}')
        print(f'Perceptos anteriores: {self.perceptos_anteriores}')
        print(f'Celdas seguras: {self.celdas_seguras}')
        print(f'Precipicios: {self.precipicios}')
        print(f'Monstruo: {self.monstruo}')
        print(f'Salida: {self.salida}')
        print('\n')
        print('Resultados inferidos (motor de inferencia): ')

        if percepto_actual[0] == 1: # Damos ciertos avisos en función del percepto actual 
            print('Cuidado puede haber un precipicio en una de las habitaciones contiguas')
            posible_precipicio = []
            adyacentes = f.obtener_adyacentes(i,j,self.n)
            for adyacente in adyacentes:
                if adyacente not in self.celdas_seguras and adyacente not in self.monstruo:
                    posible_precipicio.append(adyacente)
            print(f'El precipicio puede estar en {posible_precipicio} (si solo hay uno está aqui)')
            if len(posible_precipicio) == 1:
                self.precipicios.append(posible_precipicio[0])
        if percepto_actual[1] == 1 and self.monstruo_vivo == 1:
            print('Cuidado puede haber un monstruo en una de las habitaciones contiguas')
            posible_monstruo = []
            adyacentes = f.obtener_adyacentes(i,j,self.n)
            for adyacente in adyacentes:
                if adyacente not in self.celdas_seguras and adyacente not in self.precipicios:
                    posible_monstruo.append(adyacente)
            print(f'El monstruo puede estar en {posible_monstruo} (si solo hay uno está aqui)')
            if len(posible_monstruo) == 1:
                self.monstruo.append(posible_monstruo[0])
        if percepto_actual[2] == 1:
            posible_salida = [(i,j)]
            adyacentes = f.obtener_adyacentes(i,j,self.n)
            for adyacente in adyacentes:
                if adyacente not in self.precipicios and adyacente not in self.monstruo:
                    posible_salida.append(adyacente)
            print(f'La salida está en una de las siguientes habitaciones: {posible_salida}')
        if percepto_actual[7] == 1:
            print('El monstruo ha muerto')
        if (percepto_actual[0] == 0 and percepto_actual[1] == 0) or (percepto_actual[0] == 0 and percepto_actual[7] == 1):
            print('Las celdas adyacentes parecen seguras')
            adyacentes = f.obtener_adyacentes(i,j,self.n)
            for adyacente in adyacentes:
                if adyacente not in self.celdas_seguras:
                    self.celdas_seguras.append(adyacente)
        if (i,j) not in self.celdas_seguras:
            self.celdas_seguras.append((i,j))

        if perceptos_anteriores != {}: # En este bucle se infieren posiciones con bastante seguridad (si se siente el mismo percepto en 2 casillas adyacentes una, muy probablemente el elemento esté en esa una)
            adyacentes = f.obtener_adyacentes(i,j,self.n)
            for casilla in perceptos_anteriores: 
                percepto_anterior = perceptos_anteriores[casilla]
                if casilla == (i+2,j):
                    if percepto_actual[0] == 1 and percepto_anterior[0] == 1:
                        print(f'Hay un precipicio en la celda {(i+1,j)}')
                        self.precipicios.append((i+1,j))
                    if percepto_actual[1] == 1 and percepto_anterior[1] == 1 and self.monstruo_vivo == 1:
                        print(f'El monstruo está en la celda {(i+1,j)}')
                        self.monstruo.append(i+1,j)
                    if percepto_actual[2] == 1 and percepto_anterior[2] == 1:
                        print(f'La salida está en la celda {(i+1,j)}')
                        self.salida.append((i+1,j))
                    if (percepto_actual[0] == 0 or percepto_anterior[0] == 0) and (percepto_actual[1] == 0 or percepto_anterior[1] == 0):
                        if (i+1,j) not in self.celdas_seguras:
                            print(f'La celda {(i+1,j)} es segura')
                            self.celdas_seguras.append((i+1,j))
                elif casilla == (i-2,j):
                    if percepto_actual[0] == 1 and percepto_anterior[0] == 1:
                        print(f'Hay un precipicio en la celda {(i-1,j)}')
                        self.precipicios.append((i-1,j))
                    if percepto_actual[1] == 1 and percepto_anterior[1] == 1 and self.monstruo_vivo == 1:
                        print(f'El monstruo está en la celda {(i-1,j)}')
                        self.monstruo.append(i-1,j)
                    if percepto_actual[2] == 1 and percepto_anterior[2] == 1:
                        print(f'La salida está en la celda {(i-1,j)}')
                        self.salida.append((i-1,j))
                    if (percepto_actual[0] == 0 or percepto_anterior[0] == 0) and (percepto_actual[1] == 0 or percepto_anterior[1] == 0):
                        if (i-1,j) not in self.celdas_seguras:
                            print(f'La celda {(i-1,j)} es segura')
                            self.celdas_seguras.append((i-1,j))
                elif casilla == (i,j+2):
                    if percepto_actual[0] == 1 and percepto_anterior[0] == 1:
                        print(f'Hay un precipicio en la celda {(i,j+1)}')
                        self.precipicios.append((i,j+1))
                    if percepto_actual[1] == 1 and percepto_anterior[1] == 1 and self.monstruo_vivo == 1:
                        print(f'El monstruo está en la celda {(i,j+1)}')
                        self.monstruo.append(i,j+1)
                    if percepto_actual[2] == 1 and percepto_anterior[2] == 1 and self.salida == []:
                        print(f'La salida está en la celda {(i,j+1)}')
                        self.salida.append((i,j+1))
                    if (percepto_actual[0] == 0 or percepto_anterior[0] == 0) and (percepto_actual[1] == 0 or percepto_anterior[1] == 0):
                        if (i,j+1) not in self.celdas_seguras:
                            print(f'La celda {(i,j+1)} es segura')
                            self.celdas_seguras.append((i,j+1))
                elif casilla == (i,j-2):
                    if percepto_actual[0] == 1 and percepto_anterior[0] == 1:
                        print(f'Hay un precipicio en la celda {(i,j-1)}')
                        self.precipicios.append((i,j-1))
                    if percepto_actual[1] == 1 and percepto_anterior[1] == 1 and self.monstruo_vivo == 1:
                        print(f'El monstruo está en la celda {(i,j-1)}')
                        self.monstruo.append(i,j-1)
                    if percepto_actual[2] == 1 and percepto_anterior[2] == 1 and self.salida == []:
                        print(f'La salida está en la celda {(i,j-1)}')
                        self.salida.append((i,j-1))
                    if (percepto_actual[0] == 0 or percepto_anterior[0] == 0) and (percepto_actual[1] == 0 or percepto_anterior[1] == 0): 
                        if (i,j-1) not in self.celdas_seguras:
                            print(f'La celda {(i,j-1)} es segura')
                            self.celdas_seguras.append((i,j-1))

                    
                if (casilla in adyacentes) and (percepto_actual[2] == 1 and percepto_anterior[2] == 1): # Inferimos la posición de la salida (acortamos las posibilidades)
                    print(f'La salida esta en {casilla} o en {(i,j)}')
        self.perceptos_anteriores[(i,j)] = percepto_actual

        # Actualizamos la matriz
        self.celdas_seguras = list(set(self.celdas_seguras)) # eliminamos posibles duplicados
        self.precipicios = list(set(self.precipicios))
        self.salida = list(set(self.salida))
        self.monstruo = list(set(self.monstruo))
        for segura in self.celdas_seguras:
            i = segura[0]
            j = segura[1]
            matriz[i][j].inferido = 'Sg'  # Sg de segura
        for precipicio in self.precipicios:
            i = precipicio[0]
            j = precipicio[1]
            matriz[i][j].inferido = 'P'
        for salida in self.salida:
            i = salida[0]
            j = salida[1]
            matriz[i][j].inferido = 'S'
        for monstruo in self.monstruo:
            i = monstruo[0]
            j = monstruo[1]
            matriz[i][j].inferido = 'M'
        return matriz













