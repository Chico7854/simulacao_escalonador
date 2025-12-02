from Mutex import Mutex
from Evento import Evento

class Tarefa:
    def __init__(self, id, cor, ingresso, duracao, prioridade, lista_eventos):
        self.id = int(id)
        self.cor = "#" + cor
        self.ingresso = int(ingresso)
        self.duracao = int(duracao)
        self.prioridade = int(prioridade)
        self.prioridade_dinamica = int(prioridade)
        self.string_lista_eventos = ";".join(lista_eventos)
        self.lista_eventos = []
        self.em_suspensao = False
        self.herancaPrioridade = False
        for evento in lista_eventos:                                    # Cria lista de eventos
            tipo = evento[0:2]
            if tipo == "ML":                                     # Se evento for solicitação de mutex cria o evento
                inicio = int(ingresso) + int(evento[-2:])
                ev = Evento(inicio, "mutex")
                ev.setIdMutex(evento[2:4])
                self.lista_eventos.append(ev)
            elif tipo == "MU":                                   # Se for liberação de mutex atribui a duração
                for ev in self.lista_eventos:
                    if ev.tipo == "mutex":
                        if ev.id_mutex == evento[2:4]:
                            ev.setDuracaoMutex(evento[-2:])
            else:
                inicio = int(ingresso) + int(evento[3:5])
                ev = Evento(inicio, "IO")
                ev.setDuracaoIO(evento[-2:])

    def lock(self, id_mutex, lista_mutex):
        mutex = None
        for mu in lista_mutex:
            if id_mutex == mu.id:
                mutex = mu

        if (not mutex):                                                             # Cria um novo mutex caso não exista
            mutex = Mutex(id_mutex)
            lista_mutex.append(mutex)
    
        if (mutex.isLocked):
            if (mutex.tarefa.prioridade_dinamica < self.prioridade_dinamica):       # Herança de Prioridades
                mutex.tarefa.prioridade_dinamica = self.prioridade_dinamica
                self.em_suspensao = True
        else:
            mutex.isLocked = True
            mutex.tarefa = self
    
    def unlock(self, id_mutex, lista_mutex):
        mutex = None
        for mu in lista_mutex:
            if id_mutex == mu.id:
                mutex = mu
        
        if (not mutex):
            return

        if (mutex.tarefa == self):
            mutex.tarefa = None
            mutex.isLocked = False

    def reset(self):
        self.em_suspensao = False
        if (self.herancaPrioridade):
            self.herancaPrioridade = False
            self.prioridade_dinamica = self.prioridade