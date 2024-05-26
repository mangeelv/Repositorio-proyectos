from typing import Tuple, List, Dict
import json, hashlib, time

'''Integrantes: 
Miguel Ángel Huamai
Miguel Ángel Vallejo'''


class Bloque:
    def __init__(self, indice: int , hash: str,  transacciones: list(dict()), timestamp: int, hash_previo: str, prueba: int =0):
        '''
        Constructor de la clase `Bloque`.
        :param indice: ID unico del bloque.
        :param transacciones: Lista de transacciones.
        :param timestamp: Momento en que el bloque fue generado.
        :param hash_previo hash previo
        :param prueba: prueba de trabajo
        '''
        self.indice = indice
        self.hash = hash
        self.transacciones = transacciones
        self.timestamp = timestamp
        self.hash_previo = hash_previo
        self.prueba = prueba

    def calcular_hash(self):
        """
        Metodo que devuelve el hash de un bloque
        """
        block_string =json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def toDict(self):
        return {'indice': self.indice, 'hash': self.hash, 'transacciones': self.transacciones, 'timestamp': self.timestamp, 'hash_previo':self.hash_previo, 'prueba':self.prueba}



class Blockchain(object):
    def __init__(self):
        self.dificultad = 4
        self.lista_bloques = [] # Al principio contendrá el primer bloque 
        self.transacciones_no_confirmadas = []
    def toDict(self):
        return {'dificultad':self.dificultad, 'lista_bloques':self.lista_bloques, 'transacciones_no_confirmadas':self.transacciones_no_confirmadas}

    # Codigo a completar (inicializacion de las listas de transacciones y de
    # bloques)
    def nuevo_bloque(self, hash_previo: str) ->Bloque:
     
        """
        Crea un nuevo bloque a partir de las transacciones que no estan
        confirmadas
        :param hash_previo: el hash del bloque anterior de la cadena
        :return: el nuevo bloque
        """
        indice = len(self.lista_bloques) + 1 # El primer bloque empieza en índice 1 
        transacciones_no_confirmadas = self.transacciones_no_confirmadas
        timestamp = time.time()
        prueba = 0
        bloque = Bloque(indice,None,transacciones_no_confirmadas,timestamp,hash_previo,prueba)
        return bloque

        
    def nueva_transaccion(self, origen: str, destino: str, cantidad: int) ->int: 

        """
        Crea una nueva transaccion a partir de un origen, un destino y una
                                            cantidad y la incluye en las
            listas de transacciones :param origen: <str> el que envia la transaccion
        :param destino: <str> el que recibe la transaccion
        :param cantidad: <int> la candidad
        :return: <int> el indice del bloque que va a almacenar la transaccion
        """

        transaccion = {'origen': origen, 'destino': destino, 'cantidad ': cantidad, 'tiempo': time.time()}
        self.transacciones_no_confirmadas.append(transaccion)
        indice = len(self.lista_bloques) + 1
        return indice


    def primer_bloque(self):
        primer_bloque = Bloque(1,None,[],time.time(),1,0)
        hash_prueba = self.prueba_trabajo(primer_bloque)
        self.integra_bloque(primer_bloque,hash_prueba)
       
        


    def prueba_trabajo(self, bloque: Bloque) ->str:
              
        """Algoritmo simple de prueba de trabajo:
        - Calculara el hash del bloque hasta que encuentre un hash que empiece
                                                por tantos ceros como dificultad
        .
        - Cada vez que el bloque obtenga un hash que no sea adecuado,
                                                incrementara en uno el campo de
        ``prueba'' del bloque
        :param bloque: objeto de tipo bloque
        :return: el hash del nuevo bloque (dejara el campo de hash del bloque sin modificar)
        """
        bloque.prueba = 0 
        ceros = "0"*self.dificultad
        hash = bloque.calcular_hash()
        while hash[:self.dificultad] != ceros:
            bloque.prueba += 1
            hash = bloque.calcular_hash()
        return hash
         
    def prueba_valida(self, bloque: Bloque, hash_bloque: str) ->bool:
        """
        Metodo que comprueba si el hash_bloque comienza con tantos ceros como la
        dificultad estipulada en el
        blockchain
        Ademas comprobara que hash_bloque coincide con el valor devuelvo del
                                                metodo de calcular hash del
        bloque.
        Si cualquiera de ambas comprobaciones es falsa, devolvera falso y en caso
        :param bloque:
        contrario, verdarero
        :param hash_bloque:
        :return:
        """
        if hash_bloque != bloque.calcular_hash() or hash_bloque[:self.dificultad] != '0'*self.dificultad:
            return False
        else:
            return True


  
    def integra_bloque(self, bloque_nuevo: Bloque, hash_prueba: str) ->bool:
        """
        Metodo para integrar correctamente un bloque a la cadena de bloques.
        Debe comprobar que hash_prueba es valida y que el hash del bloque ultimo
                                                de la cadena
        coincida con el hash_previo del bloque que se va a integrar. Si pasa las
                                                comprobaciones, actualiza el hash
        del bloque nuevo a integrar con hash_prueba, lo inserta en la cadena y
        hace un reset de las
        transacciones no confirmadas (
        vuelve
        a dejar la lista de transacciones no confirmadas a una lista vacia)
        :param bloque_nuevo: el nuevo bloque que se va a integrar
        :param hash_prueba: la prueba de hash
        :return: True si se ha podido ejecutar bien y False en caso contrario (si
                                                no ha pasado alguna prueba)
        """
        if bloque_nuevo.hash_previo == 1:
            if self.prueba_valida(bloque_nuevo, hash_prueba):
                bloque_nuevo.hash = hash_prueba
                self.lista_bloques.append(bloque_nuevo)
                self.transacciones_no_confirmadas = []
                return True
        else:
            if self.prueba_valida(bloque_nuevo, hash_prueba) == True and  self.lista_bloques[-1].hash == bloque_nuevo.hash_previo:
                bloque_nuevo.hash = hash_prueba
                self.lista_bloques.append(bloque_nuevo)
                self.transacciones_no_confirmadas = []
                return True
            else:
                return False
            
        
if __name__ == '__main__':
    blckchain = Blockchain()
    blckchain.primer_bloque()
    idx_transaccion =blckchain.nueva_transaccion('A','B',3000)
    hash_previo = blckchain.lista_bloques[len(blckchain.lista_bloques)-1].hash # El hash que tiene guardado el último bloque (no sería su hash real)
    nuevo_bloque = blckchain.nuevo_bloque(hash_previo)
    hash_prueba = blckchain.prueba_trabajo(nuevo_bloque)
    print(blckchain.integra_bloque(nuevo_bloque,hash_prueba))

