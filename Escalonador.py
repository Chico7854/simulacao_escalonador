from Tarefa import Tarefa
from copy import deepcopy

class Escalonador:
    def __init__(self):
        self.tcb = []

        # Leitura do sistema_padrao.txt
        with open("sistema_padrao.txt") as f:
            cabecalho = f.readline().split(";")
            self.tipo = cabecalho[0]
            self.quantum = int(cabecalho[1])
        
            for linha in f:
                atributos = linha.split(";")
                tarefa = Tarefa(atributos[0], atributos[1], atributos[2], atributos[3], atributos[4], atributos[5])
                self.tcb.append(tarefa)

        self.qtd_tarefas = len(self.tcb)

    # Cria nova tarefa e adiciona a tcb
    def criar_tarefa(self, id, cor, ingresso, duracao, prioridade):
        tarefa = Tarefa(id, cor, ingresso, duracao, prioridade, [])
        self.tcb.append(tarefa)
        self.qtd_tarefas += 1

    # Exclui tarefa da tcb
    def excluir_tarefa(self, id):
        self.tcb = [t for t in self.tcb if t.id != int(id)]
        self.qtd_tarefas -= 1

    # Zera variaveis do escalonador
    def setup(self):
        self.tarefas = deepcopy(self.tcb)
        self.tempo = 0
        self.resetar_quantum()
        self.processador = None
        self.tarefas_prontas = []
        self.tarefas.sort(key=lambda tarefa: tarefa.id)

    # Ativa esaclonador escolhido
    def prox_tarefa(self):
        tipo_escalonador = self.tipo
        if tipo_escalonador == "FIFO":
            return self.FIFO()
        elif tipo_escalonador == "SRTF":
            return self.SRTF()
        elif tipo_escalonador == "Prioridade Preemptivo":
            return self.prio_preemp()

    # Simula FIFO
    def FIFO(self):
        self.preempcao = self.append_nova_tarefa()
        self.tempo += 1
        if len(self.tarefas_prontas) == 0:
            return None
        if (self.quantum_restante <= 0):
            self.preempcao = True
        elif (self.tarefas_prontas[0].duracao == 0):
            self.preempcao = True

        if (self.preempcao):
            self.resetar_quantum()
            tarefa_trocada = self.tarefas_prontas.pop(0)
            if (tarefa_trocada.duracao > 0):
                self.tarefas_prontas.append(tarefa_trocada)

        self.quantum_restante -= 1

        if len(self.tarefas_prontas) > 0:
            processador = self.tarefas_prontas[0]
            processador.duracao -= 1
            return processador
        else:
            return None
    
    # Simula SRTF
    def SRTF(self):
        self.preempcao = self.append_nova_tarefa()
        self.tempo += 1

        if (self.processador):
            if (self.processador.duracao <= 0):
                self.preempcao = True
                self.tarefas_prontas.remove(self.processador)
                self.processador = None

        if len(self.tarefas_prontas) == 0:
            return None

        if (self.quantum_restante <= 0):
            self.preempcao = True

        if (self.preempcao):
            self.processador = self.tarefas_prontas[0]
            for tarefa in self.tarefas_prontas:
                if (tarefa.duracao < self.processador.duracao) and (tarefa.duracao > 0):
                    self.processador = tarefa
                    
        self.processador.duracao -= 1

        return self.processador
    
    # Simula Prio Preemp
    def prio_preemp(self):
        self.preempcao = self.append_nova_tarefa()
        self.tempo += 1
        if (self.processador):
            if (self.processador.duracao <= 0):
                self.preempcao = True
                self.tarefas_prontas.remove(self.processador)
                self.processador = None

        if len(self.tarefas_prontas) == 0:
            return None

        if (self.preempcao):
            self.processador = self.tarefas_prontas[0]
            for tarefa in self.tarefas_prontas:
                if (tarefa.prioridade > self.processador.prioridade) and (tarefa.duracao > 0):
                    self.processador = tarefa

        self.processador.duracao -= 1

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
