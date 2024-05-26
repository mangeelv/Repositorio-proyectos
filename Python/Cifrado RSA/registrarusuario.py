# Programa que permite crear un nuevo usuario.
# El programa se ejecutará de la siguiente manera en una terminal:
# python registrarusuario.py
# El programa solicitará al usuario que introduzca por teclado:
# – Un nombre: <nombre>
# – El valor mínimo de cada primo usado para generar sus claves de RSA.
# – El valor máximo de cada primo usado para generar sus claves de RSA.
# – El número de cifras de padding para la comunicación con ese usuario.
# En base a estos datos, el programa generará un par de claves públicas (n, e) y privada d para RSA y creará dos ficheros:
# 1. pub_<nombre>.txt: Que contendrá 3 líneas:
# * n
# * e
# * El número de cifras de padding.
# 2. pub_<nombre>.txt:
# Que contendrá una única línea con la clave privada d.

# Se guardarán estos dos ficheros en una carpeta llamada “Usuarios” ubicada en el mismo directorio que el script.
# Si la carpeta no existe, el programa deberá crearla.

# En los materiales de la práctica se incluyen ejemplos (“pub ejemplo.txt” y “priv ejemplo.txt”) de estos dos ficheros,
# para un usuario llamado “ejemplo” cuya configuración para RSA sea:
# – n = 809570247883
# – e = 77204266853
# – d = 42840500717
# – 3 cifras de “padding”.
import rsa as rsa
import subprocess
subprocess.call(['bash', 'carpeta_usuarios_check.sh'])
num_usuarios = int(input("Introduce el número de usuarios que deseas registrar: "))
for i in range(num_usuarios):
    nombre = input("Introduce tu nombre de usuario: ")
    valor_min = int(
        input("Introduce p1 (el valor minimo de tu primo menor para generar las claves RSA): ")
    )
    valor_max = int(
        input("Introduce p2 (el valor máximo de tu primo mayor para generar las claves RSA): ")
    )
    cifras_padding = int(
        input("Introduce el número de cifras de padding para la comunicación con tu usuario: ")
    )

    lista_claves = rsa.generar_claves(valor_min, valor_max)

    with open(f"Usuarios/pub_{nombre}.txt", "w") as f1:
        f1.writelines(
            f"{lista_claves[0]}" "\n" f"{lista_claves[1]}" "\n" f"{cifras_padding}"
        )

    with open(f"Usuarios/priv_{nombre}.txt", "w") as f1:
        f1.writelines(f"{lista_claves[2]}")
