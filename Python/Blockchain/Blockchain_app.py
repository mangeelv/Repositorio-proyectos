import Blockchain
from uuid import uuid4

import socket
import requests
from flask import Flask, jsonify, request
from argparse import ArgumentParser

from threading import Thread,Semaphore
import time
import json
from threading import Semaphore

'''Integrantes: 
Miguel Ángel Huamai
Miguel Ángel Vallejo'''

# Instanciacion de la aplicacion
blockchain = Blockchain.Blockchain()
blockchain.primer_bloque()
nodos_red = set()

mutex = Semaphore(1)

# Blockchain es un recurso compartido entre el main y el hilo que hace la copia de seguridas


def obtener_direccion():
    direccion_ip = request.host.split(':')[0]
    puerto = request.host.split(':')[1]
    return f'http://{direccion_ip}:{puerto}'


# Copia de seguridad
def copia_seguridad(ip_nodo,puerto_nodo):
    global blockchain
    while True:
        mutex.acquire()
        with open(f"respaldo-nodo{ip_nodo}-{puerto_nodo}.json", "w") as file:
           data ={
                        'chain': [b.toDict() for b in blockchain.lista_bloques if b.hash is not None],
                        'longitud': len(blockchain.lista_bloques)}
           json.dump(data,file)
        mutex.release()
        
        time.sleep(60)


# Instancia del nodo
app =Flask(__name__)

@app.route('/transacciones/nueva', methods=['POST'])
def nueva_transaccion():
    global blockchain

    values = request.get_json()
    # Comprobamos que todos los datos de la transaccion estan
    required =['origen', 'destino', 'cantidad']
    if not all(k in values for k in required):
        return 'Faltan valores', 400
    # Creamos una nueva transaccion
    indice =blockchain.nueva_transaccion(values['origen'], values['destino'],
    values['cantidad'])
    response ={'mensaje': f'La transaccion se incluira en el bloque con indice {indice}'}

    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def blockchain_completa():
    global blockchain
    # Solamente permitimos la cadena de aquellos bloques finales que tienen hash
    response ={
    'chain': [b.toDict() for b in blockchain.lista_bloques if b.hash is not None],
    'longitud': len(blockchain.lista_bloques)}
    return jsonify(response), 200


@app.route('/minar', methods=['GET'])
def minar():
    
    # Recibimos un pago por minar el bloque. Creamos una nueva transaccion
    # Dejamos como origen el 0 con:
    # Destino nuestra ip
    # Cantidad = 1
    # [Completar el siguiente codigo]
    global blockchain
    # Comporbamos si hay resolución de conflictos
    if resuelve_conflictos():
        response = {
            'mensaje': 'Ha habido un conflicto. Esta cadena se ha actualizado con una versión más larga'
        }
        return jsonify(response), 200

    else:
        # No hay transacciones
        if len(blockchain.transacciones_no_confirmadas) == 0:
            response ={
            'mensaje': "No es posible crear un nuevo bloque. No hay transacciones"
            }
      
            return jsonify(response),200
        else:
            # Hay transaccion, por lo tanto ademas de minar el bloque, recibimos recompensa
            previous_hash = blockchain.lista_bloques[-1].hash
            blockchain.nueva_transaccion(0,mi_ip,cantidad = 1)
            nuevo_bloque = blockchain.nuevo_bloque(previous_hash)
            hash_prueba = blockchain.prueba_trabajo(nuevo_bloque)
                    
            if blockchain.prueba_valida(nuevo_bloque,hash_prueba):
                exito = blockchain.integra_bloque(nuevo_bloque,hash_prueba)
                if exito:
                    response = {'mensaje': 'Nuevo bloque minado', 'indice': nuevo_bloque.indice, 
                            'transacciones': nuevo_bloque.transacciones, 'prueba': nuevo_bloque.prueba, 
                            'hash_previo': nuevo_bloque.hash_previo, 'hash_nuevo_blqoue': nuevo_bloque.hash, 'time': nuevo_bloque.timestamp}      
                else:
                    response = {'mensaje': 'No ha sido posible minar el bloque'}

    
                return jsonify(response), 200


@app.route('/nodos/registrar', methods=['POST'])
def registrar_nodos_completo():
    values =request.get_json()
    global blockchain
    global nodos_red # Esto es una lista de urls 
    nodos_nuevos =values.get('direccion_nodos') # Nodos que vamos a registrar 
    for nodo in nodos_nuevos: # añadimos los nodos nuevos al set de nodos_red
        nodos_red.add(nodo) # Le metemos todos los nodos nuevos que vamos a registrar 
    if nodos_nuevos is None:
        return "Error: No se ha proporcionado una lista de nodos", 400
    all_correct =True
    #[Codigo a desarrollar]
    # Pasamos cada bloque a diccionario antes de mandarlo
    lista_bloques_dict = [b.toDict() for b in blockchain.lista_bloques if b.hash is not None] # Pasamos el objeto blockchain a diccionario y luego a json
    for nodo in nodos_nuevos:
        nodos_enviar = nodos_red # Nodos que están en la red actual menos este 
        nodos_enviar.add(obtener_direccion()) # le añadimos este 
        nodos_enviar.remove(nodo) # le quitamos el mismo 
        data = {'nodos_direcciones':list(nodos_enviar),'blockchain':lista_bloques_dict} # Pasamos nodos_red a lista 
        # Enviamos la petición a los otros nodos 
        response =requests.post(nodo
        +"/nodos/registro_simple", data=json.dumps(data), headers ={'Content-Type':
        "application/json"})
        if response.status_code != 200:
            all_correct = False
            nodo_erroneo = nodo
    # Fin codigo a desarrollar
    if all_correct:
        response ={
        'mensaje': 'Se han incluido nuevos nodos en la red',
        'nodos_totales': list(nodos_red)
        }
    else:
        response ={
        'mensaje': f'Error al registrar el nodo {nodo_erroneo}',
        }
    return jsonify(response), 201


@app.route('/nodos/registro_simple', methods=['POST'])
def registrar_nodo_actualiza_blockchain():
    global blockchain
    global nodos_red
    read_json = request.get_json() #Obetenenos la respuesta 
    nodes_addreses =read_json.get("nodos_direcciones") # Nodos que existen en la red
    for nodo in nodes_addreses: # Actualizamos la variable global 
        nodos_red.add(nodo)

    # [...] Codigo a desarrollar
    bloques_dic = read_json.get("blockchain") # Lista de bloques en formato diccionario (blockchain del 'nodo raíz')
    blockchain_leida = Blockchain.Blockchain()
    blockchain_leida.dificultad = 4 # La dificultad es la misma 
    blockchain_leida.transacciones_no_confirmadas = [] 
    # Creamos cada bloque a partir de lo que se recibe y lo metemos en una blockchain 
    for bloque_dic in bloques_dic:
        indice = bloque_dic['indice']
        hash_prueba = bloque_dic['hash'] # Al modificar el  atributo 'hash' en el bloque su verdadero hash cambia, por lo que si no lo inicializamos a none no es posible integrarlo en en blockchain
        transacciones = bloque_dic['transacciones']
        timestamp = bloque_dic['timestamp']
        hash_previo = bloque_dic['hash_previo']
        prueba = bloque_dic['prueba']
        bloque = Blockchain.Bloque(indice,None,transacciones,timestamp,hash_previo,prueba) # el atributo hash del bloque debe ser inicializado a none para que el 'hash_prueba' coincida con el verdadero hash del bloque 
        blockchain_leida.integra_bloque(bloque,hash_prueba) # Integramos en bloque (hash_prueba = bloque.calcular_hash()) ya que hash se ha puesto a None, al integrarlo se cambiará 

    #[...] fin del codigo a desarrollar
    if blockchain_leida is None:
        return "El blockchain de la red esta currupto", 400
    else:
        blockchain = blockchain_leida
        return "La blockchain del nodo " +str(mi_ip) +":" +str(puerto) +" ha sido correctamente actualizada", 200
    




def resuelve_conflictos():
    """
    Mecanismo para establecer el consenso y resolver los conflictos
    """
    global blockchain
    longitud_actual =len(blockchain.lista_bloques)
    cadena_actual = blockchain.lista_bloques
    # [Codigo a completar]
    print(nodos_red)
    for nodo in nodos_red:
        response = requests.get(str(nodo) +'/chain')
        datos = response.json()
        longitud_cadena_bloques = datos.get('longitud')
        cadena_bloques = datos.get('chain')
        
        if longitud_cadena_bloques > longitud_actual:
                longitud_actual = longitud_cadena_bloques
                cadena_actual = cadena_bloques # Formato diccionario

        if longitud_actual > len(blockchain.lista_bloques):
            blockchain.lista_bloques = []
            for bloque_dic in cadena_actual:
                indice = bloque_dic['indice']
                hash = bloque_dic['hash'] # Al modificar el  atributo 'hash' en el bloque su verdadero hash cambia, por lo que si no lo inicializamos a none no es posible integrarlo en en blockchain
                transacciones = bloque_dic['transacciones']
                timestamp = bloque_dic['timestamp']
                hash_previo = bloque_dic['hash_previo']
                prueba = bloque_dic['prueba']
                bloque = Blockchain.Bloque(indice,hash,transacciones,timestamp,hash_previo,prueba) # el atributo hash del bloque debe ser inicializado a none para que el 'hash_prueba' coincida con el verdadero hash del bloque 
                blockchain.lista_bloques.append(bloque) 
            return True  
        else:
            return False
        

        

@app.route('/ping', methods=['GET'])
def ping():
    global nodos_red

    respuestas = [] # lista para guardar todas las respuestas pong al ping 
    respuesta_final = ''
    nodos_respondido = []

    # desde el nodo que ha enviado el ping mandamos un json a cada nodo de la red 
    for nodo in nodos_red:
        print(nodo)
        datos = {'datos_host': str(mi_ip)+':'+str(puerto),
                 'mensaje': 'PING',
                 'time': time.time()}
        
        response =requests.post(nodo+"/pong", data=json.dumps(datos), headers ={'Content-Type':"application/json"}) 
        respuesta = response.json()
        respuestas.append(respuesta)
        nodos_respondido.append(respuesta['nodo'])
        print('respuesta del pong', response.json())

    # genero la respuesta final, tras haber respondido los nodos 
    respuesta_final+= '#'+respuestas[0]['mensaje_ping'] + '. Respuesta: '
    for resp in respuestas: 
        respuesta_final+= resp['respuesta'] + '. Retardo: ' + resp['retardo']

    # si todos los nodos han respondido 
    print(nodos_respondido)
    print(list(nodos_red))
    if len(nodos_respondido) == len(list(nodos_red)):
        respuesta_final += '#Todos los nodos responden'

    response = {'respuesta_final': respuesta_final}

    return jsonify(response), 200


@app.route('/pong', methods=['POST'])
def pong():
    global nodos_red
    global mi_ip
    global puerto 
    # recogemos el ping mandado
    mensaje_ping =request.get_json()
    print('Recibido ',mensaje_ping)

    retardo =time.time() - mensaje_ping['time']

    respuesta_pong = {'mensaje_ping': f"{mensaje_ping['mensaje']} de {mensaje_ping['datos_host']}",
            'respuesta': f'PONG {obtener_direccion()}',
             'retardo': f'{retardo}',
             'nodo':'http://' + str(mi_ip) + ':' + str(puerto)+'/' }
    print(respuesta_pong)
    return jsonify(respuesta_pong), 200


# Para saber mi ip
# Ip Mangel: 172.19.62.7
mi_ip ='172.19.62.7'
if __name__ =='__main__':
    puerto = 5001
    # Hilo de copia de seguridad
    hilo = Thread(target=copia_seguridad, args=(mi_ip,puerto))
    hilo.start()
    parser =ArgumentParser()
    parser.add_argument('-p', '--puerto', default=puerto, type=int, help='puerto para escuchar')
    args =parser.parse_args()
    puerto =args.puerto   
    app.run(host='0.0.0.0', port=puerto)