class Tarefa:
    def __init__(self, id, cor, ingresso, duracao, prioridade, lista_eventos):
        self.id = int(id)
        self.cor = cor
        self.ingresso = int(ingresso)
        self.duracao = int(duracao)
        self.prioridade = int(prioridade)
        self.lista_eventos = lista_eventos
