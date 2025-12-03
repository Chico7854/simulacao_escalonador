from Mutex import Mutex
from Evento import Evento

class Tarefa:
    def __init__(self, id, cor, ingresso, duracao, prioridade, lista_eventos):
        self.id = int(id)
        self.cor = "#" + cor
        self.ingresso = int(ingresso)
        self.duracao = int(duracao)
        self.tempo_decorrido = 0
        self.prioridade = int(prioridade)
        self.prioridade_dinamica = int(prioridade)
        self.string_lista_eventos = ";".join(lista_eventos)             # String para mostrar eventos na tela inicial
        self.lista_eventos_mutex = []
        self.lista_eventos_IO = []
        for evento in lista_eventos:                                    # Cria lista de eventos
            tipo = evento[0:2]
            if tipo == "ML":                                            # Se evento for solicitação de mutex cria o evento
                inicio = int(evento[-2:])
                ev = Evento(inicio, "mutex")
                ev.setIdMutex(evento[2:4])
                self.lista_eventos_mutex.append(ev)
            elif tipo == "MU":                                          # Se for liberação de mutex atribui a duração
                for ev in self.lista_eventos_mutex:
                    if ev.tipo == "mutex":
                        if ev.id_mutex == int(evento[2:4]):
                            final = int(ingresso) + int(evento[-2:])
                            ev.setDuracaoMutex(final)
            else:                                                       # Se for IO
                inicio = int(evento[3:5])
                ev = Evento(inicio, "IO")
                ev.setDuracaoIO(evento[-2:])
                self.lista_eventos_IO.append(ev)

    # Operação de Lock do Mutex, retorna None se funcionou, e o mutex se ele bloqueou
    def lock(self, evento, lista_mutex):
        mutex = None
        id_mutex = evento.id_mutex
        success = True
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
                success = False
            
        if success:
            return None
        else:
            return mutex
    
    
    def unlock(self, mutex):
        mutex.tarefa = None
        mutex.isLocked = False

    # Verifica se tem algum mutex para tratar, retorna true se tarefa conseguiu processar no mutex ou se não houver mutex, false se foi bloqueada
    def verificar_mutex(self, lista_mutex):
        for evento in self.lista_eventos_mutex:
            if evento.inicio <= self.tempo_decorrido:
                return self.lock(evento, lista_mutex)
        return None
    
    def decrementar_duracao_evento_mutex(self, lista_mutex):
        for evento in self.lista_eventos_mutex:
            if evento.inicio <= self.tempo_decorrido:
                evento.duracao -= 1
            if evento.duracao <= 0:
                self.lista_eventos_mutex.remove(evento)
                for mutex in lista_mutex:
                    if evento.id_mutex == mutex.id:
                        self.unlock(mutex)

    # Verifica e trata eventos IO
    def verificar_IO(self):
        for evento in self.lista_eventos_IO:
            if evento.inicio <= self.tempo_decorrido:
                evento.duracao -= 1
                if evento.duracao <= 0:
                    self.lista_eventos_IO.remove(evento)
                return True
        return False
    
    def decrementar_duracao(self, lista_mutex):
        self.duracao -= 1
        self.tempo_decorrido += 1
        self.decrementar_duracao_evento_mutex(lista_mutex)

    def inverter_prioridades(self, tarefa):
        temp = tarefa.prioridade_dinamica
        tarefa.prioridade_dinamica = self.prioridade_dinamica
        self.prioridade_dinamica = temp

    def resetar_prioridade(self):
        self.prioridade_dinamica = self.prioridade