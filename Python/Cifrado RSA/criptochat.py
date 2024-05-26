# “criptochat.py”: Chat encriptado extremo a extremo.
# Se ejecutará de la siguiente manera en una terminal
# python3 criptochat.py <usuario1> <usuario2>

# donde <usuario1> y <usuario2> son los nombres de dos usuarios del programa.
# El programa buscará los ficheros de claves públicas y privada de <usuario1>
# y el fichero con la clave pública de <usuario2> y cargará dichas claves.

# Si alguno no existe, se lo indicará al usuario y finalizará.
# Una vez cargadas las claves de ambos usuarios, el programa permitirá cifrar mensajes
# de parte de <usuario1> para <usuario2> o descifrar mensajes que <usuario2> haya enviado a <usuario1>.

# Para ello, el programa:
# – Preguntará al usuario si desea cifrar (C), descifrar (D) o salir (S).

# – Si el usuario escribe C: Le pedirá que escriba por teclado un texto plano e imprimirá por pantalla el correspondiente texto cifrado,
# usando para ello la clave pública de <usuario2> y el número de cifras de “padding” del <usuario2>.

# – Si el usuario escribe D: Le pedirá que escriba por teclado el texto cifrado proveniente de <usuario2>,
# lo descifrará usando la clave privada de <usuario1> y el número de cifras de “padding” de <usuario1>
# e imprimirá por pantalla el texto claro resultante.

# – Si el usuario escribe S: Saldrá del programa.

# Cada vez que se realice una acción, se volverá a preguntar si desea cifrar, descifrar o salir hasta que el usuario decida salir del programa.

# En cuanto al formato de los mensajes:
# – Los mensajes en texto plano, se introducirán e imprimirán como cadenas de texto normales.
# Ejemplo de texto plano: hola
# – Los mensajes cifrados se introducirán e imprimirán como listas de enteros separadas por espacios.
# Ejemplo de texto cifrado: 512533741 128348154 125512341 16453783 3012812 1247503 50252341

import rsa as rsa
import sys
# import registrar_usuario as us

input_args = sys.argv
usuario1 = input_args[1]   # los nombres de usuario se obtienen a partir de la ejecución por terminal 
usuario2 = input_args[2]
opcion = 0
while opcion != "S":
    opcion = input(
        "Introduce la opción que deseas realizar: Cifrar(C), Descifrar(D) o Salir(S): "
    )
    print(
        """
        Menú:
            1. Cifrar (C)
            2. Descifrar (D)
            3. Salir 
            """
    )

    if opcion == "C": # Ciframos un mensaje con las claves de usuario 2 (ciframos un mensaje para usuario 2)
        texto = input("Introduce el texto que deseas cifrar: ")
        with open(f"Usuarios/pub_{usuario2}.txt") as f1:
            claves_publicas = f1.readlines()
        n2 = int(claves_publicas[0])
        e2 = int(claves_publicas[1])
        padding2 = int(claves_publicas[2])
        texto_cifrado = rsa.cifrar_cadena_rsa(texto,n2,e2,padding2)
        print(texto_cifrado)

    elif opcion == "D": # Desciframos un mensaje para nosotros (usuario1) con nuestras claves
        texto_cifrado = input("Introduce el texto cifrado a descifrar: ")
        texto_cifrado = eval(texto_cifrado) # pasamos el texto cifrado a lista 

        conversor_int = lambda numero:int(numero) # pasámos los elementos de la lista del mensaje cifado de string a enteros
        texto_cifrado = map(conversor_int,texto_cifrado)
        texto_cifrado= list(texto_cifrado)

        with open(f"Usuarios/pub_{usuario1}.txt") as f2:
            claves_publicas = f2.readlines()
        n1 = int(claves_publicas[0])
        e1 = int(claves_publicas[1])
        padding1 = int(claves_publicas[2])
        with open(f"Usuarios/priv_{usuario1}.txt") as f3:
            d1 = int(f3.readlines()[0])

        texto_descifrado = rsa.descifrar_cadena_rsa(texto_cifrado,n1,d1,padding1)
        print(texto_descifrado)
    else:
        print("Gracias por usar el chat de encriptación.")
