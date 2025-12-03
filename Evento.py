class Evento:
    def __init__(self, inicio, tipo):
        self.inicio = int(inicio)
        self.tipo = tipo

    def setIdMutex(self, id_mutex):
        self.id_mutex = int(id_mutex)

    def setDuracaoMutex(self, fim):
        self.duracao = int(fim) - self.inicio

    def setDuracaoIO(self, duracao):
        self.duracao = int(duracao)