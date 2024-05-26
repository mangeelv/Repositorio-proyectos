class operacion:
    def __init__(self, tipo:str, entrada:list, salida:list):
        self.tipo = tipo 
        self.entrada = entrada
        self.salida = salida
    def __str__(self):
        return f" Tipo: {self.tipo} | datos de entrada: {self.entrada} | salida: {self.salida} "