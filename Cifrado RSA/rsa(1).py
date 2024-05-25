"""
rsa.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GPxxx
Integrantes:
    - XX
    - XX

Descripción:
Librería para la realización de cifrado y descifrado usando el algoritmo RSA.
"""
import modular as mod
from typing import Tuple, List
import random


def generar_claves(min_primo: int, max_primo: int) -> Tuple[int, int, int]:
    """
    Toma dos primos entre min_primo (incluido) y max_primo (excluido) y
    devuelve n,e,d donde (n,e) es la clave pública y d la clave privada para RSA

    Args:
        min_primo (int): Límite inferior para los primo p1 y p2 usados en la clave
        max_primo (int): Límite superior para los primo p1 y p2 usados en la clave


    Returns:
        n (int): Módulo para RSA, formado por el producto de dos primos p1 y p2 tales que
            min_primo<=p1, p2 < max_primo
        e (int): Exponente de la clave pública para RSA con módulo n=p1*p2
        d (int): Exponente de la clave privada para RSA con módulo n

    Raises: None
    """
    # Generamos dos primos aleatorios p1 y p2

    p1 = random.randint(min_primo, max_primo)
    p2 = random.randint(min_primo, max_primo)

    # Calculamos el módulo n como el producto de p1 y p2
    n = p1 * p2

    # phi = mod.euler(n)
    phi = (p1 - 1) * (p2 - 1)

    # Calcular el exponente e tal que e*d mod phi(n)=1

    while True:
        e = random.randint(2, phi - 1)
        comparacion = mod.coprimos(e, phi)
        if comparacion == "Sí":
            print(f"e: {e}")
            break

    d = mod.inversa_mod_p(e, phi)

    clave_publica = [n, e]
    print(f"Clave pública: {clave_publica}")
    clave_privada = d
    print(f"Clave privada: {clave_privada}")

    return n, e, d


min_primo = random.randint(1, 1000)
max_primo = random.randint(1, 1000)
print(generar_claves(min_primo, max_primo))


def aplicar_padding(m: int, digitos_padding: int) -> int:
    """
    Dado un mensaje y un número de dígitos de padding, añade
    digitos_padding cifras aleatorias a la derecha del mensaje

    Args:
        m (int): Mensaje sin padding
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero formado por los dígitos de m seguidos de digitos_padding cifras aleatorias.

    Raises: None

    Example:
        aplicar_padding(24,2)=2419
        aplicar_padding(24,2)=2403
        aplicar_padding(24,3)=24718
        aplicar_padding(24,3)=24845
    """
    for i in range(digitos_padding):
        added_digit = random.randint(1, digitos_padding)
        m = str(m) + str(added_digit)

    return m


def eliminar_padding(m: int, digitos_padding: int) -> int:
    """
    Dado un mensaje con padding de digitos_padding cifras al
    final del mismo, elimina dichas cifras aleatorias y devuelve
    el resto de cifras del mensaje

    Args:
        m (int): Mensaje con padding
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero resultante de eliminar las últimas digitos_padding cifras de m.

    Raises: None

    Example:
        aplicar_padding(2454,1)=245
        aplicar_padding(2454,2)=24
        aplicar_padding(2454,3)=2
        aplicar_padding(2432,2)=24
    """
    for i in range(digitos_padding):
        last_digit = str(m)[-1]
        m = int(str(m).rstrip(last_digit))
        # if not last_digit.isnumeric():
        #     raise ValueError("El mensaje no tiene una estructura correcta")
        # else:
        #     m = int(str(m).rstrip(last_digit))

    return m


def cifrar_rsa(m: int, n: int, e: int, digitos_padding: int) -> int:
    """
    Dado un mensaje m entero, un módulo y exponente que formen parte de una clave pública de RSA,
    con m<n*10^{-digitos_padding}, y un número de dígitos de padding, aplica el padding al mensaje
    y lo cifra usando RSA con módulo n y exponente e.

    Args:
        m (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero resultante de agregar el padding a m y aplicar RSA.

    Raises: None
    """


def descifrar_rsa(c: int, n: int, d: int, digitos_padding: int) -> int:
    """
    Dado un cifrado c entero que haya sido cifrado con RSA usando
    digitos_padding cifras de padding al final del mensaje y el
    módulo y exponente privado, n y d que formen la clave privada de RSA cuya pareja se
    utilizó para cifrar c, descifra c y elimina el padding, devolviendo
    el mensaje original.

    Args:
        c (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA usado para cifrar
        d (int): Exponente de la clave privada de RSA cuya pareja se utilizó para cifrar c
        digitos_padding (int): Número de cifras de padding usados para cifrar c


    Returns:
        int: entero resultante de descifrar c usando RSA con módulo m y exponente e y después eliminar el padding al resultado.

    Raises: None
    """
    pass


def codificar_cadena(s: str) -> List[int]:
    """
    Convierte una cadena de caracteres a la lista de
    enteros que representa el valor unicode cada uno de sus caracteres.

    Args:
        s (str): cadena en texto plano

    Returns:
        int: lista de enteros que representan el código unicode de cada carácter de la cadena s.

    Raises: None.

    Example:
        codificar_cadena("¡Hola mundo!")=[161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33]
    """
    pass


def decodificar_cadena(m: List[int]) -> str:
    """
    Convierte una lista de enteros que representen caracteres unicode
    en la cadena que representan.

    Args:
        m (List[int]): lisa de enteros que representan los códigos unicode de una cadena de caracteres.

    Returns:
        str: cadena que representan

    Raises:
        ValueError: Si alguno de los enteros no representa un caracter unicode válido.

    Example:
        decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])="¡Hola mundo!"
    """
    pass


def cifrar_cadena_rsa(s: str, n: int, e: int, digitos_padding: int) -> List[int]:
    """
    Encripta carácter a carácter una cadena de caracteres usando RSA con clave púbica (n,e)
    y digitos_padding cifras de padding al final del mensaje y devuelve la lista de enteros
    que representan el mensaje cifrado correspondiente.
    Args:
        s (str): texto claro
        n (int): módulo para RSA
        e (int): clave pública para RSA
        digitos_padding (int): número de dígitos de padding que deben usarse para el cifrado del mensaje.

    Returns:
        List[int]: lista de enteros que representa el mensaje cifrado con RSA para la clave dada.

    Raises: None
    """
    pass


def descifrar_cadena_rsa(cList: List[int], n: int, d: int, digitos_padding: int) -> str:
    """
    Dado un mensaje cifrado con RSA usando la clave pública cuya clave privada asociada es (n,d)
    y digitos_padding cifras de padding al final del mensaje, devuelve la cadena orignal.
    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        d (int): clave privada para RSA
        digitos_padding (int): número de dígitos de padding usados para el cifrado de cList.

    Returns:
        str: cadena que representa el texto claro correspondiente al mensaje cifrado cList.

    Raises:
        ValueError: Si, tras decodificar, alguno de los enteros del mensaje no representa un caracter unicode válido.
    """
    pass


def romper_clave(n: int, e: int) -> int:
    """
    A partir de una clave pública válida (n,e), recupera la clave privada d tal que
    de = 1 (mod phi(n)).

    Args:
        n (int): módulo para RSA
        e (int): clave pública para RSA

    Returns:
        int: clave privada d

    Raises:
        ValueError: Si no existe ninguna clave privada d compatible con la clave pública (n,e).
    """
    pass


def ataque_texto_elegido(cList: List[int], n: int, e: int) -> str:
    """
    Ejecuta un ataque de texto claro elegido sobre un mensaje que ha sido encriptado
    con RSA plano sin usar padding a partir de su clave pública.

    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        e (int): clave pública para RSA

    Returns:
        str: texto plano descifrado para el mensaje cifrado cList

    Raises:
        ValueError: Si el mensaje no se corresponde con ningún texto plano que haya sido codificado con RSA sin padding.
    """
    pass
