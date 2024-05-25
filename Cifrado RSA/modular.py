"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP04
Integrantes:
    - María González
    - Miguel Ángel Vallejo

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
import math
import numpy as np
import time


class IncompatibleEquationError(Exception):
    pass


def es_primo(n: int) -> bool:
    """
    Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero

    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None

    Examples:
        es_primo(5)=true
        es_primo(4)=false

    """

    if (
        n <= 0 or n == 1
    ):  # el número 1 no es primo (un primo es aquel número solo con dos divisores distintos, el mismo y 1), y estamos considerando unicamente primos naturales
        return "No"
    else:
        for i in range(
            2, round(np.sqrt(n)) + 1
        ):  # por el teorema de cota para divisores primos sabemos que si n=compuesto, existe un primo que lo divide y dicho es menor o igual que la raiz de n
            if n % i == 0:
                return "No"
        return "Sí"


def lista_primos(a: int, b: int) -> list:
    """
    Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)

    Returns:
        bool: true si el entero es un número primo. false en caso contrario.

    Raises: None

    Examples:
        lista_primos(1,11)=[2,3,5,7]

    """

    # Algoritmo: Criba de Eratóstenes

    if a < 0 and b < 0:
        return ""
    elif a < 0 and b > 0:
        a = 0  # No hay primos negativos
    maximo = b

    primo = [True] * (maximo + 1)
    primo[0], primo[1] = False, False

    for i in range(2, int(maximo**0.5) + 1):
        if primo[i]:
            for j in range(i**2, maximo + 1, i):
                primo[j] = False

    lista = [i for i in range(a, maximo + 1) if primo[i]]
    # Devolvemos el formato pedido
    salida = ""
    for i in range(len(lista)):
        salida += str(lista[i]) + ","
    salida = salida.rstrip(",")
    return salida


def factorizar(n: int) -> Dict[int, int]:
    """
    Recibe un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.

    Args:
        n (int): Entero que se desea factorizar.

    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}

    """
    # Algoritmo RHO DE POLLARD
    if n == -1 or n == 0 or n == 1:
        return n
    negativo = False
    if n < 0:
        n = -n  # Le cambiamos el signo
        negativo = True

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def pollard_rho(n):
        if n == 1:
            return 1
        if n % 2 == 0:
            return 2

        def f(x):
            return (x**2 + 1) % n

        x, y, d = 2, 2, 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        if d == n:
            return n
        else:
            return d

    factores = {}

    while n > 1:
        factor = pollard_rho(n)
        if factor:
            if factor in factores:
                factores[factor] += 1
            else:
                factores[factor] = 1
            n //= factor

    salida = ""
    if negativo:
        salida += "-"
    elif not negativo:
        salida += "+"
    for primo in factores:
        salida += str(primo) + ":" + str(factores[primo]) + ","
    salida = salida.rstrip(",")
    return salida





def mcd(a: int, b: int) -> int:
    """
    Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples
        mcd(10,15)=5
    """
    if a < 0:
        a = -a
    if b < 0:
        b = -b  # Les cambiamos el signo, los divisores serán siempre positivos
    while a != 0:
        resto = b % a
        cociente = b // a
        b = a
        a = resto
    return b


def bezout(a: int, b: int) -> Tuple[int, int, int]:
    """
    Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
    d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples
        bezout(6,10)=(2,2,-1)
    """

    # Paso 1: Inicializamos las variables

    x0 = 1  # coeficiente de a
    x1 = 0  # siguiente coeficiente de a
    y0 = 0  # coeficiente de b
    y1 = 1  # siguiente coeficiente de b

    while b:
        q = a // b  # q = Cociente de la división
        a, b = (
            b,
            a % b,
        )  # Actualizamos a y b para el siguiente paso # por lo visto en clase sabemos que (b,a) = (a,r)
        x0, x1 = x1, x0 - q * x1  # Actualizamos los coeficientes
        y0, y1 = y1, y0 - q * y1

    return (a, x0, y0)


def mcd_n(nlist: List[int]) -> int:
    """
    Dada una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.

    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples
        mcd([4,10,14])=2
    """
    # Opcional
    pass


def bezout_n(nlist: List[int]) -> Tuple[int, List[int]]:
    """
    Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
    d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.

    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    # Opcional
    pass


def coprimos(n: int, m: int) -> bool:
    """Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples
        coprimos(14,20)=false
        coprimos(14,15)=true
    """
    # aplicamos mcd
    while n != 0:
        resto = m % n
        cociente = m // n

        m = n
        n = resto

    if m == 1:
        return "Sí"
    else:
        return "No"


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.

    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0.
    """

    if p == 0:
        return "NE: El módulo no puede ser 0"
    mod_negativo = False
    if p < 0:  # Del signo del módulo dependerá el signo del resto
        p = -p
        mod_negativo = True

    # Asegurarse de que la base sea positiva
    if base < 0:
        base = base % p
    if exp == 0:
        return 1 % p

    # Manejar exponentes negativos
    if exp < 0:
        # Calcular el inverso modular de la base si es posible
        base = pow(base, -1, p)
        exp = -exp
    # Inicializar el resultado
    resultado = 1
    # Algoritmo de exponenciación rápida
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % p
        exp = exp // 2
        base = (base * base) % p
    if mod_negativo:
        return -resultado
    else:
        return resultado


def inversa_mod_p(
    n: int, p: int
) -> int:  # usamos el algorimto de euclides para resolver
    """Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.

    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    """

    if p == 0:
         return "NE: El módulo no puede ser 0"
    
    # Asegúrate de trabajar con el valor absoluto de p
    abs_p = abs(p)
    
    resto, previous_resto = n, abs_p

    x, previous_x = 1, 0
    y, previous_y = 0, 1

    while resto != 0:
        cociente = previous_resto // resto
        previous_resto, resto = resto, previous_resto - cociente * resto
        previous_x, x = x, previous_x - cociente * x
        previous_y, y = y, previous_y - cociente * y

    if previous_resto > 1:
            return "NE: n no es invertible módulo p."
    
    # Ajusta el resultado según el signo original de p
    if p < 0:
        return (-previous_x) % abs_p
    else:
        return previous_x % abs_p



def euler(n: int) -> int:
    """
    Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.

    Returns:
        int: Función phi de Euler de n.

    Raises: None
    """
    # Paso 1: factorizar el numero en primo
    n_factors = factorizar(n)  # string
    dic_n_factors = n_factors.split(",")
    simbolo = dic_n_factors[0][0]
    dic_n_factors[0] = dic_n_factors[0].lstrip(simbolo)
    dic = {}
    for elemento in dic_n_factors: # pasamos a diccionario para que euler funcione 
        elemento = elemento.split(":")
        clave = elemento[0]
        valor = elemento[1]
        dic[int(clave)] = int(valor)
    dict_n_factors = dic  # diccionario que contiene los factores del número n
    # Paso 2: Calcular la función
    funcion = 1
    for k, v in dict_n_factors.items():
        funcion *= k ** (v - 1) * (k - 1)
    return funcion




def legendre(n: int, p: int) -> int:
    """
    Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.

    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.
    """

    if p % 2 == 0 or not es_primo(p):  # p debe ser un numero primo impar
        return "NE"

    if n == 0:
        return 0  # 0 congruente con 0(p)

    elif n == 1:
        return 1  # 1 congruente con 1^2(p)

    elif n % 2 == 0:  # Si es par usamos la propiedad recursiva de legendre
        return legendre(n // 2, p) * ((-1) ** ((p**2 - 1) // 8))

    else:  # Propiedad reciprocidad cuadrática
        return legendre(p % n, n) * ((-1) ** ((n - 1) * (p - 1) // 4))


def resolver_sistema_congruencias(
    alist: List[int], blist: List[int], plist: List[int]
) -> Tuple[int, int]:
    """
    Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias

    a_i * x = b_i (mod p_i)   i=1,...,n

    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]

    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.
    """
    # Paso 1: Aplicar el mcd y verificar que los números son coprimos

    for i in range(len(plist)):
        for j in range(i + 1, len(plist)):
            if mcd(plist[i], plist[j]) != 1:
                return "NE: Los módulos no son primos relativos entre sí."  # raise IncompatibleError

    # Paso 2: Calcular el modulo global = producto de todos los números de plist

    modulo_global = 1
    for num in plist:
        modulo_global *= num

    # Paso 3: Aplicar el teorema chino y resolver el sistema (usamos bezout al resolver cada ecuación por separado)

    # x = ai*bi(modulos distintos a pi)*xi
    x = 0

    for i in range(len(alist)):
        # Inicializamos variables (a = b(p))
        ai = alist[i]
        bi = blist[i]
        pi = plist[i]

        producto_modulos = modulo_global // pi
        _, coef_bezout, _ = bezout(producto_modulos, pi)

        x += ai * coef_bezout * producto_modulos * bi

    # Paso 4: Obtenemos la solución final del sistema

    r = x % modulo_global

    return r, modulo_global


def raiz_mod_p(n: int, p: int) -> int:
    # Opcional

    """
    Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.

    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
    """


def ecuacion_cuadratica(a: int, b: int, c: int, p: int) -> Tuple[int, int]:
    # Opcional
    """Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.

    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.
    """
