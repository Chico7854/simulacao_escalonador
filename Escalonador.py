from Tarefa import Tarefa
from Mutex import Mutex
from copy import deepcopy

class Escalonador:
    def __init__(self):
        self.tcb = []

        # Leitura do sistema_padrao.txt
        with open("sistema_padrao.txt") as f:
            cabecalho = f.readline().split(";")
            self.tipo = cabecalho[0]
            self.quantum = int(cabecalho[1])
            self.alpha = int(cabecalho[2])
        
            for linha in f:
                atributos = linha.strip().split(";")
                if atributos[5] == '':
                    atributos.pop()
                tarefa = Tarefa(atributos[0], atributos[1], atributos[2], atributos[3], atributos[4], atributos[5:])
                self.tcb.append(tarefa)

        self.qtd_tarefas = len(self.tcb)

    # Cria nova tarefa e adiciona a tcb
    def criar_tarefa(self, id, cor, ingresso, duracao, prioridade):
        tarefa = Tarefa(id, cor, ingresso, duracao, prioridade, [])
        self.tcb.append(tarefa)
        self.ordenar_tarefas()
        self.qtd_tarefas += 1

    # Exclui tarefa da tcb
    def excluir_tarefa(self, id):
        self.tcb = [t for t in self.tcb if t.id != int(id)]
        self.qtd_tarefas -= 1

    def criar_evento(self, id_tarefa, tipo, ingresso, duracao):
        for tarefa in self.tcb:
            if tarefa.id == int(id_tarefa):
                tarefa.criar_evento(tipo, ingresso, duracao)

    def excluir_mutex(self, id_tarefa, id_mutex):
        for tarefa in self.tcb:
            if tarefa.id == int(id_tarefa):
                tarefa.excluir_mutex(id_mutex)

    # Zera variaveis do escalonador
    def setup(self):
        self.tarefas = deepcopy(self.tcb)
        self.tempo = 0
        self.resetar_quantum()
        self.processador = None
        self.tarefas_prontas = []
        self.lista_mutex = []
        self.prox_preempcao = False
        self.tarefas.sort(key=lambda tarefa: tarefa.id)
        self.fazendo_IO = False
        self.tarefa_trocada = None
        self.houve_heranca_prioridade = False

    # Ativa escalonador escolhido
    def prox_tarefa(self):
        tipo_escalonador = self.tipo
        if tipo_escalonador == "FIFO":
            return self.FIFO()
        elif tipo_escalonador == "SRTF":
            return self.SRTF()
        elif tipo_escalonador == "Prioridade Preemptivo":
            return self.prio_preemp()
        elif tipo_escalonador == "Prioridade Preemptivo Envelhecimento":
            return self.prio_preemp_envelhecimento();

    # Simula FIFO
    def FIFO(self):
        self.fazendo_IO = False                     # Variável para Informação no front end
        self.preempcao = self.append_nova_tarefa()  # Verifica se entrou nova tarefa para preemptar
        if self.prox_preempcao:                     # Flag da iteração passada para ter preempção
            self.prox_preempcao = False
            self.preempcao = True
        tarefaIO = self.verificar_IO_tarefas()
        self.tempo += 1
        if tarefaIO:
            self.processador = tarefaIO
            self.fazendo_IO = True
            self.prox_preempcao = True
            return tarefaIO
        
        if len(self.tarefas_prontas) == 0:      # Se não houver tarefas prontas pula
            return None
        if (self.quantum_restante <= 0):    # Verifica de o quantum acabou para preemptar
            self.preempcao = True
        elif (self.tarefas_prontas[0].duracao == 0):    # Verifica se a tarefa no processador terminou para preemptar
            self.preempcao = True

        # Em caso de preempção
        if (self.preempcao):    
            self.resetar_quantum()      # Reseta o valor do quantum
            bloqueado_mutex = True
            while bloqueado_mutex:
                tarefa_trocada = self.tarefas_prontas.pop(0)    # Tira do começo da fila a tarefa
                if (tarefa_trocada.duracao > 0):
                    self.tarefas_prontas.append(tarefa_trocada)     # Se a tarefa ainda não terminou, adiciona para o final da fila
                if len(self.tarefas_prontas) > 0:
                    bloqueado_mutex = self.tarefas_prontas[0].verificar_mutex(self.lista_mutex)

        self.quantum_restante -= 1

        if len(self.tarefas_prontas) > 0:
            processador = self.tarefas_prontas[0]
            processador.decrementar_duracao(self.lista_mutex)    # Diminui a duracao da tarefa
            return processador      # Retorna a tarefa que ocupou o processador
        else:
            return None     # Caso acabou a tarefa e nao há nenhuma tarefa na lista de prontas
    
    # Simula SRTF
    def SRTF(self):
        self.fazendo_IO = False                     # Variável para Informação no front end
        self.preempcao = self.append_nova_tarefa()      # Verifica se entrou nova tarefa para preemptar
        if self.prox_preempcao:
            self.prox_preempcao = False
            self.preempcao = True
        tarefaIO = self.verificar_IO_tarefas()
        self.tempo += 1
        if tarefaIO:
            self.processador = tarefaIO
            self.fazendo_IO = True
            self.prox_preempcao = True
            return tarefaIO

        if (self.processador):
            if (self.processador.duracao <= 0):     # Verifica se acabou a tarefa para preemptar
                self.preempcao = True
                self.tarefas_prontas.remove(self.processador)   # Remove da lista de prontas
                self.processador = None     # Limpa a variavel que guarda o processador

        if len(self.tarefas_prontas) == 0:      # Verifica se há tarefas prontas
            return None

        if (self.quantum_restante <= 0):       # Verifica se acabou o quantum para preemptar
            self.preempcao = True

        # Caso tenha preempção
        if (self.preempcao): 
            self.resetar_quantum()      
            self.processador = self.tarefas_prontas[0]
            for tarefa in self.tarefas_prontas:                 # Verifica entre as tarefas prontas qual tarefa possui a menor duracao restante
                if (tarefa.duracao < self.processador.duracao):
                    self.processador = tarefa
                    
        mutex = self.processador.verificar_mutex(self.lista_mutex)
        # Herança de "prioridades" SRTF
        if mutex:
            self.processador = mutex.tarefa
        self.processador.decrementar_duracao(self.lista_mutex)

        self.quantum_restante -= 1

        return self.processador
    
    # Simula Prio Preemp
    def prio_preemp(self):
        self.fazendo_IO = False                     # Variável para Informação no front end
        self.preempcao = self.append_nova_tarefa()  # Verifica se há nova tarefa para preemptar
        self.houve_heranca_prioridade = False
        if self.prox_preempcao:
            self.preempcao = True
            self.prox_preempcao = False
        tarefaIO = self.verificar_IO_tarefas()
        self.tempo += 1
        if (tarefaIO):
            self.processador = tarefaIO
            self.fazendo_IO = True
            self.prox_preempcao = True
            return tarefaIO

        if self.quantum_restante <= 0:
            self.resetar_quantum()
            self.preempcao = True

        if (self.processador):
            if (self.processador.duracao <= 0):                 # Verifica se a tarefa que estava no processador acabou para preemptar
                self.preempcao = True                           # Caso acabou preempta
                self.tarefas_prontas.remove(self.processador)   # Remove da lista de tarefas prontas
                self.processador = None                         # Limpa o processador

        if len(self.tarefas_prontas) == 0:                      # Verifica se há tarefas na lista de prontas
            return None

        # Caso há preempção
        if (self.preempcao):
            self.resetar_quantum()
            self.processador = self.tarefas_prontas[0]
            for tarefa in self.tarefas_prontas:                 # Verifica qual tarefa tem maior prioridade na lista de prontas
                if (tarefa.prioridade > self.processador.prioridade):
                    self.processador = tarefa

        mutex = self.processador.verificar_mutex(self.lista_mutex)
        if mutex:
            self.tarefa_trocada = self.processador
            self.processador = mutex.tarefa
            self.houve_heranca_prioridade = True
            self.prox_preempcao = True


        self.processador.decrementar_duracao(self.lista_mutex)
        self.quantum_restante -= 1

        return self.processador
    
    def prio_preemp_envelhecimento(self):
        self.fazendo_IO = False                     # Variável para Informação no front end
        self.preempcao = self.append_nova_tarefa()  # Verifica se há nova tarefa para preemptar
        self.houve_heranca_prioridade = False
        if self.prox_preempcao:
            self.prox_preempcao = False
            self.preempcao = True
        tarefaIO = self.verificar_IO_tarefas()
        self.tempo += 1
        if tarefaIO:
            self.processador = tarefaIO
            self.fazendo_IO = True
            self.prox_preempcao = True
            return tarefaIO

        if self.quantum_restante <= 0:
            self.preempcao = True

        if (self.processador):
            if (self.processador.duracao <= 0):                 # Verifica se a tarefa que estava no processador acabou para preemptar
                self.preempcao = True                           # Caso acabou preempta
                self.tarefas_prontas.remove(self.processador)   # Remove da lista de tarefas prontas
                self.processador = None                         # Limpa o processador

        if len(self.tarefas_prontas) == 0:                      # Verifica se há tarefas na lista de prontas
            return None

        # Caso há preempção
        if (self.preempcao):
            self.resetar_quantum()
            self.processador = self.tarefas_prontas[0]
            for tarefa in self.tarefas_prontas:                 # Verifica qual tarefa tem maior prioridade na lista de prontas
                if (tarefa.prioridade_dinamica > self.processador.prioridade_dinamica):
                    self.processador = tarefa
            
        mutex = self.processador.verificar_mutex(self.lista_mutex)
        if mutex:
            self.tarefa_trocada = self.processador
            self.processador = mutex.tarefa
            self.houve_heranca_prioridade = True
            self.prox_preempcao = True

        for tarefa in self.tarefas_prontas:
            if tarefa != self.processador:
                tarefa.prioridade_dinamica += self.alpha

        self.processador.decrementar_duracao(self.lista_mutex)
        self.quantum_restante -= 1

        if self.houve_heranca_prioridade:
            self.tarefa_trocada.resetar_prioridade()
        else:
            self.processador.resetar_prioridade()

        return self.processador
    
    # Verifica se tem novas tarefas criadas
    def append_nova_tarefa(self):
        tem_nova_tarefa = False
        for tarefa in self.tarefas:
            if (tarefa.ingresso == self.tempo):
                self.tarefas_prontas.append(tarefa)
                tem_nova_tarefa = True
        return tem_nova_tarefa        
    
    # Verifica se acabou o processamento de todas as tarefas
    def acabou_tarefas(self):
        for tarefa in self.tarefas:
            if tarefa.duracao > 0:
                return False
            
        return True
    
    # Reseta o valor do quantum para o original
    def resetar_quantum(self):
        self.quantum_restante = self.quantum

    # Ordena as tarefas por id
    def ordenar_tarefas(self):
        self.tcb.sort(key=lambda t: t.id)

    def resetar_tarefas(self):
        for tarefa in self.tarefas_prontas:
            tarefa.reset()

    # Verifica se tem alguma tarefa com operação IO para interromper
    def verificar_IO_tarefas(self):
        for tarefa in self.tarefas_prontas:
            if tarefa.verificar_IO(): return tarefa
        return None