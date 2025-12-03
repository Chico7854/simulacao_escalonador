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
        self.string_lista_eventos = ";".join(lista_eventos)             # String para mostrar eventos na tela inicial
        self.lista_eventos_mutex = []
        self.lista_eventos_IO = []
        self.herancaPrioridade = False
        for evento in lista_eventos:                                    # Cria lista de eventos
            tipo = evento[0:2]
            if tipo == "ML":                                            # Se evento for solicitação de mutex cria o evento
                inicio = int(ingresso) + int(evento[-2:])
                ev = Evento(inicio, "mutex")
                ev.setIdMutex(evento[2:4])
                self.lista_eventos_mutex.append(ev)
            elif tipo == "MU":                                          # Se for liberação de mutex atribui a duração
                for ev in self.lista_eventos_mutex:
                    if ev.tipo == "mutex":
                        if ev.id_mutex == int(evento[2:4]):
                            duracao_mutex = int(ingresso) + int(evento[-2:])
                            ev.setDuracaoMutex(duracao_mutex)
            else:                                                       # Se for IO
                inicio = int(ingresso) + int(evento[3:5])
                ev = Evento(inicio, "IO")
                ev.setDuracaoIO(evento[-2:])
                self.lista_eventos_IO.append(ev)

    def lock(self, evento, lista_mutex):
        mutex = None
        id_mutex = evento.id_mutex
        for mu in lista_mutex:
            if id_mutex == mu.id:
                mutex = mu

        if (not mutex):                                                             # Cria um novo mutex caso não exista
            mutex = Mutex(id_mutex)
            lista_mutex.append(mutex)
    
        if (not mutex.isLocked):
            mutex.isLocked = True
            mutex.tarefa = self
        else:
            if (mutex.tarefa != self):
                if (mutex.tarefa.prioridade_dinamica < self.prioridade_dinamica):       # Herança de Prioridades
                    temp = mutex.tarefa.prioridade_dinamica
                    mutex.tarefa.prioridade_dinamica = self.prioridade_dinamica
                    self.prioridade_dinamica = temp
                    self.herancaPrioridade = True
                    mutex.tarefa.herancaPrioridade = True
            
        if self.herancaPrioridade:
            return mutex.tarefa
        else:
            return self
    
    def unlock(self, mutex):
        mutex.tarefa = None
        mutex.isLocked = False

    # Verifica se tem algum mutex para tratar, retorna true se tarefa conseguiu processar no mutex ou se não houver mutex, false se foi bloqueada
    def verificar_mutex(self, tempo_atual, lista_mutex):
        for evento in self.lista_eventos_mutex:
            print(f"Id: {self.id}, Inicio: {evento.inicio}, TAtual: {tempo_atual}, Duração: {evento.duracao}")
            if evento.inicio < tempo_atual:
                return self.lock(evento, lista_mutex)
        return self
    
    def decrementar_duracao_evento_mutex(self, tempo_atual, lista_mutex):
        for evento in self.lista_eventos_mutex:
            if evento.inicio < tempo_atual:
                evento.duracao -= 1
            if evento.duracao <= 0:
                self.lista_eventos_mutex.remove(evento)
                for mutex in lista_mutex:
                    if evento.id_mutex == mutex.id:
                        self.unlock(mutex)

    def reset(self):
        if (self.herancaPrioridade):
            self.herancaPrioridade = False
            self.prioridade_dinamica = self.prioridade