import funcioneskb as fkb
import objetoskb as obkb
import funcionesby as fby
import objetosby as obby 





if __name__ == '__main__':
    n = 6
    opcion = 0 
    while True: 
        opcion = int(input('1: KB 2: Bayes 3: Salir '))
        if opcion == 1:
            entorno = fkb.crear_entorno(n)
            entorno = fkb.codificar_perceptos(entorno,n)
            capitan_willard = obkb.Capitan_Willard()
            fkb.jugar(entorno,capitan_willard,n)
        elif opcion == 2:
            entorno = fby.crear_entorno(n)
            entorno = fby.codificar_perceptos(entorno,n)
            capitan_willard = obby.Capitan_Willard()
            fby.jugar(entorno,capitan_willard,n)
        else:
            break


