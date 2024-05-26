import requests
import json

url_nodo = 'http://192.168.1.127:5000' # Nodo en el que se realizan las pruebas 
nodos_red = ["http://192.168.1.127:5001"]  
# Cabecera JSON (comun a todas)
cabecera ={'Content-type': 'application/json', 'Accept': 'text/plain'}
# datos transaccion
transaccion_nueva ={'origen': 'nodoA', 'destino': 'nodoB', 'cantidad': 10}
r =requests.post(f'{url_nodo}'+'/transacciones/nueva', data =json.dumps(
transaccion_nueva), headers=cabecera) # probamos la funcion transaccion nueva
print(r.text)
r =requests.get(f'{url_nodo}'+'/minar') # Probamos la función minar
print(r.text)
r =requests.get(f'{url_nodo}'+'/chain') # Probamos la función de obtener cadena 
print(r.text)
nodos_registrar = { "direccion_nodos": nodos_red }
r = requests.post(f'{url_nodo}'+'/nodos/registrar', data = json.dumps(nodos_registrar), headers=cabecera) # Registramos los nodos 
print(r.text)
r = requests.get(f'{url_nodo}'+'/ping') # Probamos el ping 
print(r.text)



# Prueba de resolver conflictos 

# Modificamos la blockchain de un nodo 
r =requests.post(f'{url_nodo}'+'/transacciones/nueva', data =json.dumps(
transaccion_nueva), headers=cabecera)
r =requests.get(f'{url_nodo}'+'/minar')

# intentamos minar en otros nodos 
for nodo in nodos_red:
    r =requests.get(f'{nodo}'+'/minar') # Se actualizarian las blockchain
    print(r.text)




