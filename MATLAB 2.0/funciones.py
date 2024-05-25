## Importamos paquetes 
from tkinter import *
import objetos as ob
import excepciones as excp 
import math 
import numpy as np 
import pickle 
def operar_raicespol(ae:Entry,be:Entry,ce:Entry)->tuple:
    ''' Devuelve las raíces del polinomio a partir de los datos de entrada 
        Args: ae, be, ce
        Returns: s1,s2
        Raises: excp.Polinomio_Error("Eso no es un polinomio"), excp.Polinomio_Error("Ese polinomio no tiene raíces")'''
    try:   ## Posible error: el usuario no mete un número 
        a = float(ae.get())        
        b = float(be.get())
        c = float(ce.get())
    except ValueError:
         raise excp.Polinomio_Error("Eso no es un polinomio")
    s1 = "no existe"
    s2 = "no existe"
    if a == 0.0 and b == 0.0:   ## Posible error: el usuario mete algo sin raíces
        raise excp.Polinomio_Error("Ese polinomio no tiene raíces")
    elif a == 0 and b != 0:
        s1 = -c / b
    elif b == 0.0 and a != 0.0:
        if c < 0.0:
            s1 = (math.sqrt(- c / a))
            s2 = -(math.sqrt(- c / a))
        if  c > 0.0:
            i = math.sqrt(-(-c/a))
            s1 = complex(0, i)
            s2 = complex(0, -i)
    elif a != 0.0 and b != 0.0:
        r = ((b**2)-4*a*c)
        if r > 0.0:
            s1 = (- b + math.sqrt(r)) / (2*a)
            s2 = (- b - math.sqrt(r)) / (2*a) 
        if r < 0.0:  #Si las soluciones son complejas
            i = math.sqrt(-r)
            s1 = (complex(-b, i)) / (2*a)
            s2 = (complex(-b, -i)) / (2*a)
    return s1, s2
def operar_conversor_bin_pol(x:Entry,y:Entry)->str:
    '''Devuelve la forma polar de un complejo a partir de los datos de entrada
        Args: x, y
        Returns: m, a 
        Raises: raise excp.Complex_Error("Por favor, introduce solo números")'''
    pi = math.pi
    try:
        x = float(x.get())        
        y = float(y.get())
    except ValueError:
         raise excp.Complex_Error("Por favor, introduce solo números")
    m = math.sqrt(x**2+y**2)  # módulo del complejo
    if x > 0:
        a = math.atan(y/x) #argumento del complejo
    elif x < 0:
        a = math.atan(y/x) + pi
    elif x == 0:
        if y > 0:
            a = pi/2
        else:
            a = -pi/2
    return m, a
def operar_conversor_pol_bin(validar_sqrt:str, validar_pi:str, m:Entry, a, i, p, d) ->tuple:   # a, i, p, d se pueden mandar como floats o como Entrys
    '''Devuelve la forma binómica de un complejo a partir de los datos de entrada
        Args: validar_sqrt, validar_pi, m, a, i, p, d
        Returns: pr, pi, m, a
        Raises: excp.Complex_Error("Por favor introduce números"), excp.Complex_Error("El índice de una raíz debe ser un número distinto de 0"), excp.Complex_Error("Por favor, comprueba que no estés dividiendo por 0 o introduciendo algo que no sea un número")'''
    pi = math.pi
    try:
        m = float(m.get())
    except ValueError as error:
        raise excp.Complex_Error("Por favor introduce números")
    if validar_pi == "no":
        try:
            a = float(a.get())
        except ValueError as error:
            raise excp.Complex_Error("Por favor introduce números")
    if validar_sqrt == "si":
        try:
            i = i.get()
            i = float(i)
            m = m**(1/i)
        except ZeroDivisionError:
            raise excp.Complex_Error("El índice de una raíz debe ser un número distinto de 0")
        except ValueError:
            raise excp.Complex_Error("El índice de una raíz debe ser un número distinto de 0")
    if validar_pi == "si":
        try: 
            p = float(p.get())
            d = float(d.get())
            a = (pi*p)/d
        except ValueError:
            raise excp.Complex_Error("Por favor, comprueba que no estés dividiendo por 0 o introduciendo algo que no sea un número")
        except ZeroDivisionError:
            raise excp.Complex_Error("Por favor, comprueba que no estés dividiendo por 0 o introduciendo algo que no sea un número")
    pr = m*math.cos(a)
    pi = m*math.sin(a)
    return pr, pi, m, a
def operar_raices_complejo(m:float,a:float,n:int)->list:
    '''Obtiene las raíces de un complejo
    Args: m, a, n
    Returns: lista
    Raises: no '''
    pi=math.pi
    k=0
    lista = list()
    while k <= n-1:
            lista.append(f"W{k} = ({m**(1/n)},{(a+2*pi*k)/n})")
            k += 1
    return lista
def operar_diferencias_estables(sucesion_int:list)->str:
    '''Aplica el método de las diferencias estables para obtener el término general de una sucesión
        Args: sucesion_int
        Returns: f"El término general de la sucesión es {solucion}", "La sucesión no viene dada por un polinomio o no hay suficientes elementos"
        Raises: no '''
    lista_restas = sucesion_int.copy()
    diferencias_estabilizadas = False
    cont = 0
    while not diferencias_estabilizadas:
        longitud = len(lista_restas) 
        for i in range(len(lista_restas) - 1):  # Bucle que hace las restas 
            lista_restas.append(lista_restas[i+1] - lista_restas[i])
        lista_restas = lista_restas[longitud:] #Quitamos la lista anterior
        for i in range(len(lista_restas)): # Bucle que verifica si todos los elementos de la lista son iguales 
            if lista_restas[0] == lista_restas[i]:
                diferencias_estabilizadas = True
            else:
                diferencias_estabilizadas = False
                break
        cont +=1
    tg_polinomio = False
    if len(lista_restas) > 1:
        tg_polinomio = True 
    if tg_polinomio:
        Bc = [] # Base canónica   
        for i in range(cont+1):
            Bc.insert(0, f"n^{i}")
        A = []  # Matriz de coeficientes
        for n in range(1, cont+2):
            fila = []
            for i in range(cont+1):
                fila.insert(0,n**i)
            A.append(fila)
        A = np.array(A)
        B = [] # Matriz de términos independientes
        for i in range(cont+1):
            B.append([sucesion_int[i]])
        B = np.array(B)
        C = np.linalg.inv(A).dot(B) # Resolvemos el sistema
        C = C.tolist() # Convertimos C en una lista
        for i in range(len(C)): # Corregimos imprecisiones con round 
            C[i] = str(round(C[i][0]))
        solucion = ""  # Sacamos el polinomio solución 
        for i in range(len(C)):
            solucion = solucion + f" {C[i]}*{Bc[i]} +"
        solucion = solucion[0:len(solucion)-1]
        return f"El término general de la sucesión es {solucion}"
    else: 
        raise excp.Error_diferencias_estables
def operar_clasificador_de_sistemas(A:Entry,B:Entry)->str:
    '''Clasifica un sistema por Rouché
        Args: A, B
        Returns: f"SCD con soluciones {C}", f"SCI con {numero_incognitas-rg_A} grado/os de libertad", "SI"
        Raises: excp.Error_clasificador_sistemas("Los vectores deben tener la misma dimensión y estar formados exclusivamente por números"),excp.Error_clasificador_sistemas("El número de términos independientes y de vectores ha de ser el mismo"),excp.Error_clasificador_sistemas("Solamente se pueden introducir números separados por !")  '''
    A = str(A.get())  # Matriz de coeficientes
    A = A.split("!")
    for i in range(len(A)):
        A[i] = A[i].split(" ")
    for i in range(len(A)): # Bucle que comprueba que la dimension de los vectores de la matriz sea la misma y que estos estén compuestos exclusivamente de números
        if len(A[0]) == len(A[i]):
            error_A = False 
        else: 
            error_A = True 
            break 
        try:
            for n in range(len(A[i])):
                A[i][n] = float(A[i][n])
        except ValueError:
            error_A = True
            break     
    if error_A:
        raise excp.Error_clasificador_sistemas("Los vectores deben tener la misma dimensión y estar formados exclusivamente por números")
    else:
        numero_incognitas = len(A[0])
        num_vectores = len(A)
        B = str(B.get()) # Matriz de términos independientes 
        B = B.split(" ") 
        if len(B) != num_vectores:
            raise excp.Error_clasificador_sistemas("El número de términos independientes y de vectores ha de ser el mismo")
        else:
            error_B = False
            for i in range(len(B)):
                try:
                    B[i] = float(B[i])
                except ValueError:
                    error_B = True
                    break
            if error_B:
                raise excp.Error_clasificador_sistemas("Solamente se pueden introducir números separados por !")
            else:
                for i in range(len(B)):
                    B[i] = [B[i]]
                A_ampliada = A.copy()
                for i in range(num_vectores):
                    A_ampliada[i] = A[i] + B[i]
        A = np.array(A)  # Evaluamos rangos
        B = np.array(B)
        A_ampliada = np.array(A_ampliada)
        rg_A = np.linalg.matrix_rank(A)
        rg_A_ampliada = np.linalg.matrix_rank(A_ampliada)
        if rg_A == rg_A_ampliada == numero_incognitas:
            C = np.linalg.inv(A).dot(B)
            return f"SCD con soluciones {C}"
        elif rg_A == rg_A_ampliada < numero_incognitas:
            return f"SCI con {numero_incognitas-rg_A} grado/os de libertad"
        elif rg_A != rg_A_ampliada:
                return "SI"
def operar_binomio_newton(b:Entry,n:Entry)->str:
    '''Desarolla el binomio de newton a partir de los datos de entrada
    Args: b, n
    Returns: f"(x+{b})^{n} = {desarrollo[:len(desarrollo)-1]}"
    Raises:  raise excp.Error_binomio("Inserta números enteros"), raise excp.Error_binomio("n debe ser positivo")  '''
    try:
        b = int(b.get())
        n = int(n.get())
    except ValueError:
        raise excp.Error_binomio("Inserta números enteros")
    if n <= 0:
        raise excp.Error_binomio("El número al que está elevado el binomio debe ser positivo")
    a = 1
    triangulo = [] # triángulo de Pascal
    for i in range(n+1):
        fila = []
        for j in range(i+1):
            if j == 0 or j == i:
                fila.append(1)
            else:
                fila.append(triangulo[i-1][j-1]+triangulo[i-1][j])
        triangulo.append(fila)
    fila_deseada = triangulo[-1]
    desarrollo = ""
    for i in range(n+1):
        desarrollo = f"{desarrollo} {(a**(n-i))*(b**i)*fila_deseada[i]} * x^{n-i} +"
    return f"(x+{b})^{n} = {desarrollo[:len(desarrollo)-1]}"
def operar_mcm_mcd(numero_1:Entry,numero_2:Entry):
    numero_1 = numero_1.get()
    numero_2 = numero_2.get()
    try:
        numero_1 = int(numero_1)
        numero_2 = int(numero_2)
    except ValueError:
        raise excp.Error_mcd_mcm("Por favor introduce números")
    lista_primos = []
    def es_primo(numero:int)->bool:
        ''' Devuelve un True o un False dependiendo de si el argumento es primo
        Args: numero
        Returns: False, True
        Raises: no'''
        for  i in range(2, numero): # comprobamos que no sea divisible por ninguno de los números anteriores
            if numero % i == 0:
                return False
        return True
    def obtener_factores(numero:int,lista_primos:list)->list:
        '''Descompone factorialmente un número
        Args: numero, lista_primos
        Returns: factores
        Raises: no'''
        factores = []
        while True:
            for numero_primo in lista_primos:
                if numero % numero_primo == 0:
                    factores.append(numero_primo)
                    numero = numero // numero_primo
                    break
            if numero in lista_primos:
                factores.append(numero)
                break
        return factores
    def obtener_mcm_y_mcd(factores_1:list, factores_2:list)->tuple:
        '''Funcion que obtiene el mcm y mcd de 2 números a partir de su descomposición factorial, 
        mediante bucles, condicionales y diccionarios factor:exponente
        Args: factores_1, factores_2
        Raises: no
        Returns: (mcd, mcm) '''
        dic_1 = {}
        for i in range(len(factores_1)):
            dic_1[factores_1[i]] = factores_1.count(factores_1[i])
        dic_2 = {}
        for i in range(len(factores_2)):
            dic_2[factores_2[i]] = factores_2.count(factores_2[i])
        if len(dic_1) > len(dic_2): # Definimos el diccionario grande y el pequeño
            dic_grande = dic_1.copy()
            dic_pequeno = dic_2.copy()
        else:
            dic_grande = dic_2.copy()
            dic_pequeno = dic_1.copy()
        dic_final_mcm = dic_grande.copy()
        # mcm
        for clave_grande in dic_grande: # Nos quedamos con un diccionario final que contiene las máximas frecuencias
            for clave_pequeno in dic_pequeno:
                if clave_grande == clave_pequeno:
                    clave = clave_grande
                    if dic_grande[clave] < dic_pequeno[clave]:
                        dic_final_mcm[clave] = dic_pequeno[clave]
        mcm = 1
        for clave in dic_final_mcm:
            mcm = mcm *  (clave**dic_final_mcm[clave])    
        #mcd
        dic_final_mcd = {}
        for clave_grande in dic_grande: # Nos quedamos con un diccionario final que contiene las máximas frecuencias
            for clave_pequeno in dic_pequeno:
                if clave_grande == clave_pequeno:
                    clave = clave_grande
                    if dic_grande[clave] < dic_pequeno[clave]:
                        dic_final_mcd[clave] = dic_grande[clave]
                    else:
                        dic_final_mcd[clave] = dic_pequeno[clave]
        mcd = 1
        for clave in dic_final_mcd:
            mcd = mcd *  (clave**dic_final_mcd[clave])  
        return mcm, mcd
    for numero in range(2, max(numero_1, numero_2)+10):
        if es_primo(numero):
            lista_primos.append(numero)
    if numero_1 and numero_2 in lista_primos: # Si los numeros son primos
        mcd = 1
        if numero_1 == numero_2:
            mcm = numero_1
        else:
            mcm = numero_1 * numero_2
        tupla = (mcm,mcd)
    elif numero_1 == 1 or numero_2 == 1: # si está el 1
        mcd = 1
        if numero_1 == 1:
            mcm = numero_2
        else:
            mcm = numero_1
        tupla = (mcm,mcd)
    elif numero_1 == 0 or numero_2 ==0: #si esta el 0
        mcm = 0
        if numero_1 == 0:
            mcd = numero_2
        else:
            mcm = numero_1
        tupla = (mcm,mcd)
    else:
        factores_1 = obtener_factores(numero_1,lista_primos)
        factores_2 = obtener_factores(numero_2, lista_primos)
        tupla = obtener_mcm_y_mcd(factores_1, factores_2)
    return tupla
def guardar_operaciones(operacion_tipo:str, datos_entrada:list, salida:list):
    '''Guarda las operaciones en un fichero txt y en oro fichero binario (en este caso las guarda como objeto)
        Args: operacion, datos_entrada, salida
        Returns: no
        Raises: no'''
    fichero = open("fichero_operaciones.txt", "r")    # fichero txt
    contenido = fichero.read()
    fichero.close()
    fichero = open("fichero_operaciones.txt", "w")  
    fichero.write(f"{contenido}\n")
    fichero.write(f"{operacion_tipo} Entrada:{datos_entrada} Salida:{salida}")
    fichero.close()
    datos_leidos = list()  # fichero binario
    operacion = ob.operacion(operacion_tipo, datos_entrada, salida)
    def leerbinario(fichero_bin) ->list:
        ''' Lee el fichero binario
        Args: fichero_bin
        Returns: datos_leidos
        Raises: no'''
        try:
            while True:
                datos = pickle.load(fichero_bin)
                datos_leidos.append(datos)
        except EOFError:
           pass
        return datos_leidos 
    with open("fichero_operaciones_binario.obj", "rb") as fichero_bin:
        leer = leerbinario(fichero_bin)
    with open("fichero_operaciones_binario.obj", "wb") as fichero_bin:  #Escribimos el contenido anterior
        for i in range(len(leer)):
                pickle.dump(leer[i], fichero_bin)
        pickle.dump(operacion, fichero_bin) # Escribimos el contenido nuevo 
    
            

            


                

            