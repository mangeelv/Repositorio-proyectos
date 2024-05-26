if __name__ == "__main__":
    '''Las funciones definidas aquí son exclusivamente para pedir y validar datos de entrada y mostrar por pantalla resultados del programa'''
    from tkinter import * ## Importamos paquetes 
    import funciones as f 
    import excepciones as excp 
    import objetos as ob 
    import numpy as np 
    import pickle
    root = Tk()    # Definimos la raíz de la interfaz gráfica
    root.title("Matlab 2.0") #título de la ventana
    root.config(cursor="arrow")
    root.config(bg="red")
    root.config(bd=15)
    root.config(relief="ridge")
    root.state('zoomed') # hace que la raiz se abra en pantalla completa 
    label = Label(root, text="MATLAB 2.0")   #título
    label.pack(anchor=CENTER)
    label.config(fg="white",    
                bg="black",   
                font=("Verdana",24)) 
    frame = Frame(root, width=500, height=500)  # Definimos el marco
    frame.pack(fill='both', expand=1) # Que se expanda por toda la pantalla donde no hay botones
    frame.config(cursor="arrow")
    frame.config(bg="black")
    frame.config(bd=25)
    frame.config(relief="sunken")
    frame.grid_propagate(False) # Que no modifique su tamaño
    frame.pack_propagate(False)
    with open("fichero_operaciones_binario.obj", "wb") as fichero: # Limpiamos ficheros
        pass
    fichero = open("fichero_operaciones.txt", "w")
    fichero.close()
    contador = 1 # contador de la función cont, que se usa en la función mostrar_otras_funcionalidades 
    def clear_frame():
        ''' Elimina todos los widgets del frame, para que 
        no se acumulen elementos en pantalla
        Args: no
        Returns: no
        Raises: no '''
        for widgets in frame.winfo_children():
            widgets.destroy()
    def cont():
        '''Contador global que aumenta su valor cada vez que se acciona el botón mostrar otras funcionalidades, 
        este luego es enviado como argumento a mostrar_otras_funcionalidades que muestra unos botones u otros en función de su valor
        Args: no
        Raises: no 
        Returns: no'''
        global contador
        contador += 1
    def mostrar_otras_funcionalidades(contador:int, lista_botones:list):
        '''El objetivo de esta función es que no se acumulen botones en pantalla. Muestra u oculta botones en la raíz en 
        función del parámetro contador
        Args: contador, lista_botones
        Raises: no
        Returns: no'''
        if contador % 2 != 0:
            for i in range(4):
                lista_botones[i].pack_forget()
            for i in range(4,8):
                lista_botones[i].pack()
        elif contador % 2 == 0:
            for i in range(4,8):
                lista_botones[i].pack_forget()
            for i in range(4):
                lista_botones[i].pack()
    def raices_pol():
        '''Obtiene las raíces de un polinomio de grado menor o igual a 2
        Args: no
        Returns: no
        Raises: no'''
        Label(frame, text="Inserta el término que multiplica a x^2").pack() # obtenemos los términos 
        ae = Entry(frame)            #así se piden cosas por pantalla 
        ae.pack()
        Label(frame, text="Inserta el término que multiplica a x^1").pack() 
        be = Entry(frame)
        be.pack()
        Label(frame, text="Inserta el término que multiplica a x^0").pack() 
        ce = Entry(frame)
        ce.pack()
        def mostrar_soluciones(ae:Entry, be:Entry, ce:Entry):
            ''' Muestra las raíces del polinomio por pantalla
            Args: ae, be, ce
            Returns: no
            Raises: no'''
            try:
                soluciones = f.operar_raicespol(ae,be,ce)
                s1 = soluciones[0]
                s2 = soluciones[1]
                Label(frame, text= s1, bg = "black", fg = "white").pack() 
                Label(frame, text= s2, bg = "black", fg = "white").pack()
                datos_entrada = [ae.get(), be.get(), ce.get()]
                salida = [s1, s2]
                operacion = "Raices polinomio grado menor o igual que 2"
                f.guardar_operaciones(operacion,datos_entrada,salida)  # Guardamos la operación
            except excp.Polinomio_Error as error:
                Label(frame, text= error, bg = "black", fg = "white").pack() # Mostramos el texto de error por pantalla
        Button(frame, text="Operar", command=lambda:[mostrar_soluciones(ae,be,ce)]).pack()
    def conversor_bin_pol(raices:bool,n:int):
        '''Convierte un complejo de forma binómica a polar
            Args: raices, n
            Returns: no
            Raises: no'''
        Label(frame, text="Inserta la parte real").pack() 
        x = Entry(frame)           
        x.pack()
        Label(frame, text="Inserta la parte imaginaria").pack() 
        y = Entry(frame)
        y.pack()
        def mostrar_soluciones(x:Entry,y:Entry,raices:bool):
            '''Muestra las soluciones por pantalla en función de los parámetros
                Args: x, y, raices
                Returns: no
                Raises: no'''
            try:
                tupla = f.operar_conversor_bin_pol(x,y) # tupla es una tupla con el módulo y al argumento del complejo
                if not raices:
                    solucion = f"El número en forma polar es :({tupla[0]}, {tupla[1]})"
                    Label(frame, text= solucion, bg = "black", fg = "white").pack() 
                    operacion = "Conversor de complejos: binomica a polar"
                    datos_entrada = [x.get(), y.get()]
                    salida = [tupla]
                    f.guardar_operaciones(operacion, datos_entrada, salida)  # Guardamos operacion
                else:
                    lista_raices = f.operar_raices_complejo(tupla[0], tupla[1],n)
                    for elemento in lista_raices:
                        Label(frame, text= elemento, bg = "black", fg = "white").pack()
                    operacion_tipo = "Raices de un complejo"
                    datos_entrada = [tupla, n]
                    salida = lista_raices
                    f.guardar_operaciones(operacion_tipo, datos_entrada, salida)  # Guardamos operacion
            except excp.Complex_Error as error:
                Label(frame, text= error, bg = "black", fg = "white").pack() 
        Button(frame, text="Operar", command=lambda:[mostrar_soluciones(x,y,raices)]).pack()
    # Conversor de complejos: polar a binómica 
    def conversor_pol_bin(raices:bool,n:int): 
        '''Convierte un complejo de forma polar a binómica
            Args: raices, n
            Returns: no
            Raises: no'''
        Label(frame, text = "El módulo tiene raíz (si o no)").pack()  # Preguntamos como van a ser los datos de entrada 
        validar_sqrt = Entry(frame)           
        validar_sqrt.pack()
        Label(frame, text = "El argumento tiene el numero pi (si o no)").pack() 
        validar_pi = Entry(frame)           
        validar_pi.pack()
        def obtener_datos(validar_sqrt:str, validar_pi:str):
            ''' Función que obtiene datos por pantalla
            Args: validar_sqrt,validar pi
            Returns: no
            Raises: no'''
            def mostrar_resultados(validar_sqrt:str, validar_pi:str, m:Entry, a, i, p, d, raices:bool):    # a, i, p, d se pueden mandar como floats o como Entrys
                ''' Funcion que muestra los resultados por pantalla 
                Args: validar_sqrt,validar pi, m, a, i, p, d, raices
                Returns: no
                Raises: no'''
                try:
                    tupla = f.operar_conversor_pol_bin(validar_sqrt, validar_pi, m, a, i, p, d)
                    if not raices:
                        Label(frame, text =f"El numero en forma binómica es ({tupla[0]} + {tupla[1]}*i)" , bg = "black", fg = "white").pack()
                        operacion = "Conversor de complejos: polar a binomica" # guardamos operacion
                        datos_entrada = [f"raiz: {validar_sqrt}",f"pi: {validar_pi}", f"modulo: {m} (si hay raiz es lo que esta dentro)", f"indice de la raiz {i}", f"numero que multiplica a pi {p}", f"numero que divide a pi{d}" ]
                        salida = tupla
                        f.guardar_operaciones(operacion, datos_entrada, salida)
                    else:
                        lista_raices = f.operar_raices_complejo(tupla[2], tupla[3],n)
                        for elemento in lista_raices:
                            Label(frame, text= elemento, bg = "black", fg = "white").pack()
                        operacion = "Raices de un complejo" # guardamos operacion
                        datos_entrada = [f"raiz: {validar_sqrt}",f"pi: {validar_pi}", f"modulo: {m} (si hay raiz es lo que esta dentro)", f"indice de la raiz {i}", f"numero que multiplica a pi {p}", f"numero que divide a pi{d}" ]
                        salida = lista_raices
                        f.guardar_operaciones(operacion, datos_entrada, salida)
                except excp.Complex_Error as error:
                    Label(frame, text= error, bg = "black", fg = "white").pack()
            error_validar = True  # Validamos que ambas variables sean si o no 
            if error_validar: 
                validar_sqrt = str(validar_sqrt.get())
                validar_pi = str(validar_pi.get())
                if (validar_sqrt != "si" and validar_sqrt != "no") or (validar_pi != "si" and validar_pi != "no"):
                    Label(frame, text= "Pof favor, introduce si o no", bg = "black", fg = "white").pack()   
                else:
                    error_validar = False
            if not error_validar:
                i = "no existe"  # Definimos las siguentes variables, estan serán modificadas, como hay varios casos y pueden ser
                p = "no existe"  # modificadas dentro de otra función, las definimos aquí para mandarlas como argumento 
                d = "no existe"
                a = "no existe"
                if validar_sqrt == "si":  # Estructura de condicionales en función de cómo van a ser los datos de entrada escogidos por el usuario 
                    Label(frame, text="inserte numero que va dentro de la raiz").pack() 
                    m = Entry(frame)           
                    m.pack()
                    Label(frame, text="inserte el indice").pack() 
                    i = Entry(frame) 
                    i.pack()
                elif validar_sqrt == "no":
                    Label(frame, text="inserte el módulo").pack() 
                    m = Entry(frame)           
                    m.pack()
                if validar_pi == "si":
                    Label(frame, text = "por que numero quiere multiplicar pi").pack() 
                    p = Entry(frame)           
                    p.pack()
                    Label(frame, text = "entre que numero quieres dividir pi").pack() 
                    d = Entry(frame) 
                    d.pack()
                elif validar_pi == "no":
                    Label(frame, text = "inserte el argumento").pack() 
                    a = Entry(frame)           
                    a.pack()
                Button(frame, text="Mostrar resultados", command=lambda:[mostrar_resultados(validar_sqrt, validar_pi, m, a, i, p, d,raices)]).pack()
        Button(frame, text="Enviar datos", command=lambda:[obtener_datos(validar_sqrt, validar_pi)]).pack()
    def raices_complejo():
        '''Obtiene las raíces de un complejo
            Args: no
            Returns: no
            Raises: no'''
        Label(frame, text = "El complejo está en forma polar (si o no)").pack() 
        polar = Entry(frame)           
        polar.pack()
        Label(frame, text = "Inserta el índice a partir del cual quieres calcular las raices").pack() 
        n = Entry(frame)           
        n.pack()
        def obtener_datos(polar:Entry,n:Entry):
            '''Obtiene datos por pantalla y los envía las funciones que convierten complejos para obtener más datos
            Args: polar, n
            Returns: no
            Raises: no'''
            error_datos = True
            if error_datos: 
                polar = str(polar.get())
                if (polar != "si" and polar != "no"):
                    Label(frame, text= "Pof favor, introduce si o no", bg = "black", fg = "white").pack()   
                else:
                    try:
                        n = int(n.get())
                        error_datos = False
                    except ValueError:
                        Label(frame, text= "El índice debe ser un número", bg = "black", fg = "white").pack() 
            if not error_datos:
                if polar == "no":
                    conversor_bin_pol(True,n) # Mandamos estos parámetros a las funciones de conversión, 
                elif polar == "si":            # dado que la obtención de datos es la misma. 
                    conversor_pol_bin(True,n)   # Cuando se muestran los resultados, se llama a una función u otra dependiendo de los parámetros enviados
        Button(frame, text="Enviar datos", command=lambda:[obtener_datos(polar, n )]).pack()
    def diferencias_estables():
        '''Aplica el método de las diferencias estables a una sucesión de números enteros
            Args: no
            Returns: no
            Raises: no'''
        Label(frame, text = "Inserta la sucesión separada por espacios").pack() 
        sucesion = Entry(frame)           
        sucesion.pack()
        def mostrar_resultado(sucesion:Entry): 
            '''Muestra resultados por pantalla 
            Args: sucesion
            Returns: no
            Raises: no'''
            try:
                sucesion = sucesion.get()
                sucesion = sucesion.split(" ") 
                sucesion_int = []
                for i in range(len(sucesion)):
                    sucesion_int.append(int(sucesion[i]))
                solucion = f.operar_diferencias_estables(sucesion_int)
                Label(frame, text= solucion, bg = "black", fg = "white").pack()
                operacion = "Diferencias estables"
                datos_entrada = [sucesion_int]
                salida = [solucion]
                f.guardar_operaciones(operacion, datos_entrada, salida)
            except ValueError:
                Label(frame, text= "Inserta solo números separados entre sí por espacios", bg = "black", fg = "white").pack()
            except excp.Error_diferencias_estables: 
                Label(frame, text= '''No ha sido posible obtener el término general\n
                (Comprueba que hay suficientes términos)\n
                (También puede suceder que el término general no esté definido por un polinomio)''', bg = "black", fg = "white").pack()
        Button( frame, text = "Mostrar resultado", command = lambda: [mostrar_resultado(sucesion)]).pack()
    def clasificador_de_sistemas():
        '''Clasifca sistemas de ecuaciones por el método de Rouché
            Args: no
            Returns: no
            Raises: no'''
        Label(frame, text = "Introduce los vectores de la matriz, cada elemento separado por espacios y cuando se pase a otro vector indiquese con !").pack() 
        A = Entry(frame)           
        A.pack()
        Label(frame, text = "Introduce los términos independientes separados por espacios").pack() 
        B = Entry(frame)           
        B.pack()
        def mostrar_resultados(A:Entry, B:Entry):
            '''Muestra resultados por pantalla
            Args: A, B
            Returns: no
            Raises: no'''
            try:
                solucion = f.operar_clasificador_de_sistemas(A,B)
                Label(frame, text = solucion,bg = "black", fg = "white").pack() 
                operacion = "Clasificador de sistemas" # guardamos operacion
                datos_entrada = [A.get(), B.get()]
                salida = [solucion]
                f.guardar_operaciones(operacion,datos_entrada,salida)
            except excp.Error_clasificador_sistemas as error: 
                Label(frame, text = error,bg = "black", fg = "white").pack() 
        Button( frame, text = "Mostrar resultados", command = lambda: [mostrar_resultados(A,B)]).pack()
    def binomio_newton():
        '''Desarrolla un binomio por el método de Newton
        Args: no
        Returns: no
        Raises: no'''
        Label(frame, text="Inserta el número que acompaña a x").pack()
        b = Entry(frame)           
        b.pack()
        Label(frame, text="Inserta el número al que está elevado el binomio").pack()
        n = Entry(frame)           
        n.pack()
        def mostrar_resultados(b:Entry,n:Entry):
            '''Muestra resultrados por pantalla
            Args: b, n
            Returns: no
            Raises: no'''
            try:
                solucion = f.operar_binomio_newton(b,n)
                Label(frame, text = solucion,bg = "black", fg = "white").pack() 
                operacion = "Binomio de newton" # guardamos operacion
                datos_entrada = [b.get(), n.get()]
                salida = [solucion]
                f.guardar_operaciones(operacion,datos_entrada,salida)
            except excp.Error_binomio as error:
                Label(frame, text = error,bg = "black", fg = "white").pack() 
        Button( frame, text = "Mostrar resultados", command = lambda: [mostrar_resultados(b,n)]).pack()
    def mcm_mcd():
        '''Obtiene el minimo común múltiplo y el máximo común divisor de 2 números
        Args: no
        Returns: no
        Raises: no'''
        Label(frame, text="Inserta el primer número").pack()
        numero_1 = Entry(frame)           
        numero_1.pack()
        Label(frame, text="Inserta el segundo número").pack()
        numero_2 = Entry(frame)           
        numero_2.pack()
        def mostrar_resultados(numero_1:Entry, numero_2:Entry):
            '''Muestra los resultados por pantalla
            Args: numero_1, numero_2
            Returns: no
            Raises: no'''
            try:
                solucion = f.operar_mcm_mcd(numero_1,numero_2)
                Label(frame, text = f"El MCM es: {solucion[0]} | EL MCD es: {solucion[1]} ",bg = "black", fg = "white").pack()
                operacion = "MCD y MCM" # guardamos operacion
                datos_entrada = [numero_1.get(), numero_2.get()]
                salida = [solucion]
                f.guardar_operaciones(operacion,datos_entrada,salida)
            except excp.Error_mcd_mcm as error:
                Label(frame, text = error,bg = "black", fg = "white").pack() 
        Button( frame, text = "Mostrar resultados", command = lambda: [mostrar_resultados(numero_1,numero_2)]).pack()
    def mostrar_operaciones():
        '''Muestra las operaciones guardadas en fichero_operaciones_bin.obj (también lo podemos cambiar para que muestre a partir del txt)
            Args: no
            Returns: no
            Raises: no'''
        titulo = Label(frame, text="Historial de operaciones: ")
        titulo.pack(anchor=CENTER)
        titulo.config(fg="red",    # Foreground
                bg="black",   # Background
                font=("Verdana",10))
        '''  # Por si queremos que se muestren las operaciones a partir del fichero txt
        fichero = open("fichero_operaciones.txt", "r")
        lineas = fichero.readlines()
        fichero.close()
        for i in range(len(lineas)):
            lineas[i].rstrip("\n")
        for i in range(len(lineas)):
            Label(frame, text = lineas[i],bg = "black", fg = "white").pack() '''
        datos_leidos = list() # binario
        def leerbinario(fichero_bin):
            try:
                while True:
                    datos = pickle.load(fichero_bin)
                    datos_leidos.append(datos)
            except EOFError:
                pass
            return datos_leidos 
        with open("fichero_operaciones_binario.obj", "rb") as fichero_bin:
            leer = leerbinario(fichero_bin)
        for i in range(len(leer)):
            Label(frame, text = leer[i],bg = "black", fg = "white").pack() 
    limpiar = Button( root, text="Limpiar marco de trabajo", command = clear_frame)  # Botones
    limpiar.pack(side=LEFT)
    mostrar = Button( root, text="Historial", command = mostrar_operaciones)
    mostrar.pack(side=RIGHT)
    lista_botones = [] 
    boton_1 = Button( root, text = "Raíces de un polinomio de grado menor o igual que 2.", command = lambda: [raices_pol()])
    lista_botones.append(boton_1)
    boton_2 = Button( root, text = "Conversor de complejos: binómica a polar", command = lambda: [conversor_bin_pol(False,0)])
    lista_botones.append(boton_2)
    boton_3 = Button( root, text = "Conversor de complejos: polar a binómica", command = lambda: [conversor_pol_bin(False,0)])
    lista_botones.append(boton_3)
    boton_4 = Button( root, text = "Raíces de un complejo", command = lambda: [raices_complejo()])
    lista_botones.append(boton_4)
    boton_5 = Button( root, text = "Diferencias estables", command = lambda: [diferencias_estables()])
    lista_botones.append(boton_5)
    boton_6 = Button( root, text = "Clasificador de sistemas", command = lambda: [clasificador_de_sistemas()])
    lista_botones.append(boton_6)
    boton_7 = Button( root, text = "Binomio de Newton", command = lambda: [binomio_newton()])
    lista_botones.append(boton_7)
    boton_8 = Button( root, text = "MCM y MCD", command = lambda: [mcm_mcd()])
    lista_botones.append(boton_8)
    Button( root, text = "Mostrar las otras funcionalidades",background="black",foreground="white",height=2, command = lambda: [mostrar_otras_funcionalidades(contador, lista_botones ),cont()]).pack()
    mostrar_otras_funcionalidades(2,lista_botones) # para que se muestren los botones 1 al 4 nada más iniciarse la aplicación
    root.mainloop() #Bucle de la aplicación