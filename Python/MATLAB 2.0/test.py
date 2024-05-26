import funciones as f  # En este módulo testeamos un par de funciones
try:
    salida = f.operar_raices_complejo(3.0,2.0,4)
    print("operar_raices_complejo OK")
    print(salida)
except:
    print("Error en operar_raices_complejo")

try:
    salida = f.operar_diferencias_estables([2,4,6,8,10])
    print("operar_diferencias_estables OK")
    print(salida)
except:
    print("Error en operar_diferencias_estables")