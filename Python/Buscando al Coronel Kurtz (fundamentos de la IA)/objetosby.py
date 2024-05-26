# Miguel Ángel Vallejo
'''
Librería en la que se definen objetos (BY)
'''
import funcionesby as f

class Habitacion(): # Esta será nuestra clase 'estado'
    def __init__(self,elementos:str):
        self.capitan = 'X'
        self.elementos = elementos
        self.perceptos = [0,0,0,0,0,0,0,0,0,0]  # fuego pinchos dardos monstruo salida arriba abajo izquierda derecha grito
        self.posicion = None
    def __str__(self):
        return f'{self.capitan}'
    



class Capitan_Willard(): 
    def __init__(self):
        self.posicion = [0,0]
        self.dardo = 1
        self.coronel_encontrado = 0 
        self.perceptos_anteriores = {} # diccionario posicion:percepto
        self.celdas_seguras = []
        self.seguras_trampas = []
        self.seguras_salida = []
        self.seguras_monstruo = []
        self.trampas = []
        self.monstruo = []
        self.monstruo_vivo = 1
        self.salida = []
        self.n = 6
    
    def moverse(self,matriz:list,accion:str):
        '''Implementación de los movimientos del agente en el entorno'''
        if accion == 'w' and matriz[self.posicion[0]][self.posicion[1]].perceptos[5] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[0] -= 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 's' and matriz[self.posicion[0]][self.posicion[1]].perceptos[6] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[0] += 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 'a' and matriz[self.posicion[0]][self.posicion[1]].perceptos[7] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[1] -= 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        elif accion == 'd' and matriz[self.posicion[0]][self.posicion[1]].perceptos[8] == 0:
            self.celdas_seguras.append((self.posicion[0],self.posicion[1]))
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'X'
            self.posicion[1] += 1
            matriz[self.posicion[0]][self.posicion[1]].capitan = 'CW'
        else:
            print('Hay una pared, prueba otra cosa')
        return matriz

    def disparar_dardo(self,matriz:list,direccion:str,n:int):
        if self.dardo == 1:
            i = self.posicion[0]
            j = self.posicion[1]
            print('Disparo realizado')
            if i-1 >= 0  and 'M' in matriz[i-1][j].elementos and direccion == 'w':
                matriz[i-1][j].elementos.remove('M')
                matriz[i][j].perceptos[9] = 1 # Grito
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif i+1 <= n-1 and 'M' in matriz[i+1][j].elementos and direccion == 's':  
                matriz[i+1][j].elementos.remove('M')
                matriz[i][j].perceptos[9] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif j+1 <= n-1 and 'M' in matriz[i][j+1].elementos and direccion == 'd':
                matriz[i][j+1].elementos.remove('M')
                matriz[i][j].perceptos[9] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            elif j-1 >= 0 and 'M' in matriz[i][j-1].elementos and direccion == 'a':
                matriz[i][j-1].elementos.remove('M')
                matriz[i][j].perceptos[9] = 1
                self.monstruo = []
                self.monstruo_vivo = 0
                print('El monstruo ha muerto')
            else:
                print('El monstruo sigue vivo') # No hay grito
            self.dardo -= 1
        else:
            print('No quedan dardos')
        return matriz
    def salir(self,matriz:list):
        '''Implementación de la acción salir'''
        i = self.posicion[0]
        j = self.posicion[1]
        if 'S' in matriz[i][j].elementos:
            return 1
        else:
            return 0
    def mapas_probabilidad(self,matriz:list):
        n = self.n
        i = self.posicion[0]
        j = self.posicion[1]
        percepto_actual = matriz[i][j].perceptos
        mapas_mostrar = {'mapa_trampas':None,'mapa_monstruo':None,'mapa_salida':None}
        # celdas seguras
        adyacentes = f.obtener_adyacentes(i,j,n)
    
        for adyacente in adyacentes:
            if percepto_actual[0] ==0 and percepto_actual[1] == 0 and percepto_actual[2] == 0:
                self.seguras_trampas.append(adyacente)
            if percepto_actual[3] == 0:
                self.seguras_monstruo.append(adyacente)
            if percepto_actual[4] == 0:
                self.seguras_salida.append(adyacente)

        self.seguras_trampas.append((i,j))
        self.seguras_monstruo.append((i,j))
        # self.seguras_salida.append((i,j))
        self.seguras_trampas = list(set(self.seguras_trampas))
        self.seguras_monstruo = list(set(self.seguras_monstruo))
        self.seguras_salida = list(set(self.seguras_salida))
        def crear_mapa():
            mapa = []
            for i in range(n):
                lista = []
                for j in range(n):
                    lista.append(0)
                mapa.append(lista)
            return mapa
        mapa_trampas = crear_mapa()
        mapa_monstruo = crear_mapa()
        mapa_salida = crear_mapa()
        modificados = [0,0,0,0,0] # Fuego pinchos dardos monstruo salida
        if self.monstruo_vivo == 0:
            mapas_mostrar['mapa_monstruo'] = mapa_monstruo
            modificados[3] = 1
        # Caso 1: El capitán percibe estímulo
        def modificar_mapa1(self,mapa:list,tipo:str):
            adyacentes = f.obtener_adyacentes(self.posicion[0],self.posicion[1],n)
            adyacentes_inseguras = []
            for adyacente in adyacentes:
                if tipo == 'tr':
                    if adyacente not in self.seguras_trampas:
                        adyacentes_inseguras.append(adyacente)
                elif tipo == 'm':
                    if adyacente not in self.seguras_monstruo:
                        adyacentes_inseguras.append(adyacente)
                elif tipo == 's':
                    if adyacente not in self.seguras_salida:
                        adyacentes_inseguras.append(adyacente)
            num_adyacentes_inseguras = len(adyacentes_inseguras)
            try:
                probabilidad = 1/num_adyacentes_inseguras
            except ZeroDivisionError:
                probabilidad = None
            for adyacente_insegura in adyacentes_inseguras:
                mapa[adyacente_insegura[0]][adyacente_insegura[1]] = probabilidad
            mapa[self.posicion[0]][self.posicion[1]] = 'CW'
        
            return mapa
    
        if percepto_actual[0] == 1 or percepto_actual[1] == 1 or percepto_actual[2] == 1: # Trampas
            for i in range(3):
                if percepto_actual[i] == 1:
                    modificados[i] = 1
                    mapa_trampas = modificar_mapa1(self,mapa_trampas,'tr')
                mapas_mostrar['mapa_trampas'] = mapa_trampas
        
        if percepto_actual[3] == 1 and modificados[3] == 0: # Monstruo
            modificados[3] = 1
            mapa_monstruo = modificar_mapa1(self,mapa_monstruo,'m')
            mapas_mostrar['mapa_monstruo'] = mapa_monstruo
        
        if percepto_actual[4] == 1: # Salida
            modificados[4] = 1
            mapa_salida = modificar_mapa1(self,mapa_salida,'s')
            mapas_mostrar['mapa_salida'] = mapa_salida

        # Caso 2: El capitán NO percibe estímulo
        N = n*n
         

        def modificar_mapa2(self,mapa:list,tipo:str):
            adyacentes = f.obtener_adyacentes(self.posicion[0],self.posicion[1],n) # En este caso todas las adyacentes son seguras
            # Considerando que las casillas con elemento también presentan el estímulo: 
            if tipo == 'tr':
                seguras = self.seguras_trampas
            elif tipo == 'm':
                seguras = self.seguras_monstruo
            elif tipo == 's':
                seguras = self.seguras_salida
            numero_casillas_posibles_adyacentes_con_estimulo = len(adyacentes) +1 # casos favorables
            casillas_totales_posibles_que_pueden_presentar_estimulo = N  # casos totales
            prior = 1/(N-len(list(set(seguras)))) # Probabilidad de elemento en la posicion i j
            probabilidad_de_percibir_estimulo_en_posicion_actual = numero_casillas_posibles_adyacentes_con_estimulo/casillas_totales_posibles_que_pueden_presentar_estimulo
            probabilidad_de_no_percibir_estimulo_en_posicion_actual =  1 - probabilidad_de_percibir_estimulo_en_posicion_actual
            posterior = (1*prior)/probabilidad_de_no_percibir_estimulo_en_posicion_actual # Posterior para las no adyacentes, probabilidad de elemento dada la ausencia de estímulo
            for i in range(n):
                for j in range(n):
                    if (i,j) not in seguras:
                        mapa[i][j] += posterior
            mapa[self.posicion[0]][self.posicion[1]] = 'CW'
            return mapa
        for i in range(3): # trampas
            if percepto_actual[i] == 0 and modificados[i] == 0:
                mapa_trampas = modificar_mapa2(self,mapa_trampas,'tr')
            mapas_mostrar['mapa_trampas'] = mapa_trampas
        if percepto_actual[3] == 0 and modificados[3] == 0: # monstruo
            mapa_monstruo = modificar_mapa2(self,mapa_monstruo,'m')
            mapas_mostrar['mapa_monstruo'] = mapa_monstruo
        if percepto_actual[4] == 0 and modificados[4] == 0: # salida
            mapa_salida = modificar_mapa2(self,mapa_salida,'s')
            mapas_mostrar['mapa_salida'] = mapa_salida
        c = 1
        for mapa in mapas_mostrar.keys():
            if c == 1:
                print(f'Celdas sin trampa: {self.seguras_trampas}')
            elif c==2:
                print(f'Celdas sin monstruo: {self.seguras_monstruo}')
            else:
                print(f'Celdas sin salida: {self.seguras_salida}')
            mapa_name = mapa.split(('_'))[1]
            print(f'Heatmap {mapa_name}')
            f.visualizar_entorno(mapas_mostrar[mapa])
            c+=1

                




        






      


        

            








        self.perceptos_anteriores[self.posicion[0],self.posicion[1]] = percepto_actual

        

        
            
        

        