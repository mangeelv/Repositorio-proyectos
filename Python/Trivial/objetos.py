class jugador:
    def _init_(self, nombre):
        self.nombre = nombre
        self.posicion = None # guarda el valor de la casilla donde está el jugador
        self.ent = None
        self.hist = None # quesos
        self.art = None
        self.geo = None
        self.dep = None
        self.cien = None
        self.ganar = None
    def __str__(self) -> str:
        str = (f"Nombre: {self.nombre}, posicion{self.posicion.numero},entretenimiento: {self.ent}, historia: {self.hist}, arte: {self.art}, geografia: {self.geo}, deporte: {self.dep}, ciencia: {self.cien}")
        return str
class casilla:
    def _init_(self, preguntas:dict,fin:bool):
        self.preguntas = preguntas
        self.next = None
        self.prev = None
        self.numero = None # indica el numero de casilla
        self.fin = fin # True: es el último nodo (el último que se metió en el tablero) False: no lo es
        self.especial = None # No hace halta crear casillas especiales, se complicaría la lógica de movimientos. Distinguimos 2 tipos de objetos casillas, especiales y no especiales.
        self.queso = None
        self.categoria = None
    def __str__(self):
        str=(f"Casilla: {self.numero},categoria: {self.categoria} fin: {self.fin}, especial: {self.especial}, queso: {self.queso}")        
        return str  # categoria:{self.preguntas['results'][0]['category']}
class Tablero:
    def __init__(self):
        self.head = None
        self.tail = None
    def anadirnodo(self,nodo:casilla): 
        if self.head is None:
            self.head = nodo   
            self.tail = nodo 
        else: 
            nodo.next = None # El nodo del final no tiene nada detrás
            nodo.prev = self.tail # El nodo del final tiene delante a lo que antes era el final
            self.tail.next = nodo # El siguiente a lo que antes era el final es el nodo que meto
            self.tail = nodo # Actualizo el tail de la lista al nodo que acabo de meter por detrás 
        if nodo.fin:
            self.tail = self.head # cerramos el círculo
            nodo.next = self.head
            self.head.prev = nodo
    def mostrar_tablero(self):
        current = self.head
        i = 0
        while not current.fin:
            print(f"{i}: {current}")
            current = current.next
            i+=1
        print(f"{i}: {current}") # Chapuza para que muestre el último


