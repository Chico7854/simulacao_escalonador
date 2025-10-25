import tkinter
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tarefa import Tarefa

class UI:
    def __init__(self, escalonador):
        self.escalonador = escalonador
        self.root = tkinter.Tk()
        self.var_info = tkinter.StringVar()
        self.setup()
        self.root.mainloop()

    # Cria menu principal
    def setup(self):
        self.root.title("Simulação Escalonador")
        self.root.geometry("1366x768")

        # Criar label de informação do escalonador e tarefas
        self.info_label = tkinter.Label(self.root, textvariable=self.var_info, justify="left")
        self.info_label.pack(pady=20)
        self.atualizar_info()

        # Cria botão para alterar escalonador e tarefas
        botao_alterar_info = tkinter.Button(self.root, text="Editar Informações do Sistema", bg="red", command=self.editar_info)
        botao_alterar_info.pack(pady=20)

        # Criar botões para iniciar simulação
        frame_botoes = tkinter.Frame(self.root)
        frame_botoes.pack(pady=20)
        botao_simulacao_passo_a_passo = tkinter.Button(frame_botoes, text="Simulação Passo a Passo", bg="red", command=self.setup_simulacao_passo_a_passo)
        botao_simulacao_passo_a_passo.pack(side="left", padx=10)
        botao_simulacao_completa = tkinter.Button(frame_botoes, text="Simulação Completa", bg="red", command=self.setup_simulacao_completa)
        botao_simulacao_completa.pack(side="left", padx=10)

    # Cria janela para editar informações do sistema
    def editar_info(self):
        root_tarefa = tkinter.Toplevel(self.root)
        root_tarefa.geometry("1366x768")

        # Informações escalonador
        frame_escalonador = tkinter.Frame(root_tarefa)
        tkinter.Label(frame_escalonador, text="Editar Escalonador", fg="red", font=("bold")).pack()
        tkinter.Label(frame_escalonador, text="Tipo Escalonador").pack()
        opcoes_escalonador = ["FIFO", "SRTF", "Prioridade Preemptivo"]
        tipo_escalonador_combobox = ttk.Combobox(frame_escalonador, values=opcoes_escalonador)
        tipo_escalonador_combobox.pack()
        tkinter.Label(frame_escalonador, text="Quantum").pack()
        quantum_entry = tkinter.Entry(frame_escalonador)
        quantum_entry.pack()
        tkinter.Button(frame_escalonador, text="Atualizar Escalonador", bg="red", command=lambda: self.atualizar_escalonador(tipo_escalonador_combobox.get(), 
                                                                                                                             quantum_entry.get())).pack(pady=20)

        # Informações nova tarefa
        frame_criar_tarefa = tkinter.Frame(root_tarefa)
        tkinter.Label(frame_criar_tarefa, text="Criar Nova Tarefa", fg="red", font=("bold")).pack()
        tkinter.Label(frame_criar_tarefa, text="Id").pack()
        id_entry_criar = tkinter.Entry(frame_criar_tarefa)
        id_entry_criar.pack()
        tkinter.Label(frame_criar_tarefa, text="Ingresso").pack()
        ingresso_entry = tkinter.Entry(frame_criar_tarefa)
        ingresso_entry.pack()
        tkinter.Label(frame_criar_tarefa, text="Duração").pack()
        duracao_entry = tkinter.Entry(frame_criar_tarefa)
        duracao_entry.pack()
        tkinter.Label(frame_criar_tarefa, text="Prioridade").pack()
        prioridade_entry = tkinter.Entry(frame_criar_tarefa)
        prioridade_entry.pack()
        tkinter.Label(frame_criar_tarefa, text="Cor").pack()
        cor_entry = tkinter.Entry(frame_criar_tarefa)
        cor_entry.pack()
        tkinter.Button(frame_criar_tarefa, bg="red", text="Criar Tarefa", command=lambda: self.criar_tarefa(id_entry_criar.get(), cor_entry.get(), ingresso_entry.get(),
                                                                                                            duracao_entry.get(), prioridade_entry.get())).pack(pady=20)

        # Excluir tarefa
        frame_excluir_tarefa = tkinter.Frame(root_tarefa)
        tkinter.Label(frame_excluir_tarefa, text="Excluir Tarefa", fg="red", font=("bold")).pack()
        tkinter.Label(frame_excluir_tarefa, text="Id").pack()
        id_entry_excluir = tkinter.Entry(frame_excluir_tarefa)
        id_entry_excluir.pack()
        tkinter.Button(frame_excluir_tarefa, text="Excluir Tarefa", bg="red", command=lambda: self.excluir_tarefa(id_entry_excluir.get())).pack(pady=20)

        frame_escalonador.pack(side="left", expand=True, fill="both")
        frame_criar_tarefa.pack(side="left", expand=True, fill="both")
        frame_excluir_tarefa.pack(side="left", expand=True, fill="both")

    # Atualiza as informações do escalonador
    def atualizar_escalonador(self, tipo, quantum):
        self.escalonador.tipo = tipo
        self.escalonador.quantum = int(quantum)
        self.atualizar_info()

    # Cria nova tarefa
    def criar_tarefa(self, id, cor, ingresso, duracao, prioridade):
        self.escalonador.criar_tarefa(id, cor, ingresso, duracao, prioridade)
        self.atualizar_info()

    # Exclui tarefa existente
    def excluir_tarefa(self, id):
        print("Here")
        self.escalonador.excluir_tarefa(id)
        self.atualizar_info()

    # Atualiza as informações no menu principal
    def atualizar_info(self):
        tarefas = self.escalonador.tarefas
        info = "Escalonador: " + self.escalonador.tipo + "; Quantum: " + str(self.escalonador.quantum) + ";\n"
        for tarefa in tarefas:
            info += "Tarefa " + str(tarefa.id) + "; Cor: " + tarefa.cor + "; Ingresso: " + str(tarefa.ingresso) + "; Duração: " + str(tarefa.duracao) + "; Prioridade: " + str(tarefa.prioridade) + ";\n"
        self.var_info.set(info) 

    # Cria a janela da simulação, essa função vai ser usada tanto para criar a simulação passo a passo e a completa
    def setup_simulacao(self):
        self.escalonador.setup()

        self.root_simulacao = tkinter.Toplevel(self.root)
        self.root_simulacao.geometry("1366x768")
        self.fig = Figure(figsize=(13, 7))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root_simulacao)
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("Tarefas")
        self.ax.set_ylim(0.5, self.escalonador.qtd_tarefas + 0.5)
        self.ax.set_yticks(range(1, self.escalonador.qtd_tarefas + 1))

    # Cria janela especifica para simulacao passo a passo
    def setup_simulacao_passo_a_passo(self):
        self.setup_simulacao()
        self.root_simulacao.title("Simulação Passo a Passo")
        self.relogio = 0
        self.var_info_simulacao = tkinter.StringVar()
        self.next_button = tkinter.Button(self.root_simulacao, text="Next", bg="red", command=self.simulacao_passo_a_passo)
        self.info_simulacao = tkinter.Label(self.root_simulacao, textvariable=self.var_info_simulacao)

        # Organiza layout
        self.canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        self.info_simulacao.pack(pady=10)
        self.next_button.pack(side="bottom")
        
    # Cria janela especifica para simulacao completa
    def setup_simulacao_completa(self):
        self.setup_simulacao()
        self.root_simulacao.title("Simulação Completa")
        self.next_button = tkinter.Button(self.root_simulacao, text="Começar Simulação", bg="red", command=self.simulacao_completa)

        # Organiza Layout
        self.canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        self.next_button.pack(side="bottom")

    # Realiza a simulação completa
    def simulacao_completa(self):
        while(not self.escalonador.acabou_tarefas()):
            processador = self.escalonador.prox_tarefa()
            tempo_atual = self.escalonador.tempo
            tarefas_em_espera = list(self.escalonador.tarefas_prontas)
            tarefas_em_espera.remove(processador)

            # Desenha tarefas em espera
            for tarefa in tarefas_em_espera:
                self.ax.broken_barh([(tempo_atual - 1, 1)], (tarefa.id * 1 - 0.3, 0.6), facecolors="white", edgecolors="black")

            # Desenha tarefa no processador
            self.ax.broken_barh([(tempo_atual - 1, 1)], (processador.id * 1 - 0.3, 0.6), facecolors=processador.cor, edgecolors="black")   

            # Ajusta o gráfico
            self.ax.set_xlim(0, tempo_atual)
            self.ax.set_xticks(range(0, tempo_atual + 1))
            self.canvas.draw()

    # Realiza a simulação passo a passo
    def simulacao_passo_a_passo(self):
        if (self.escalonador.acabou_tarefas()):
            return
        processador = self.escalonador.prox_tarefa()
        self.atualizar_info_simulacao()
        tempo_atual = self.escalonador.tempo
        tarefas_em_espera = list(self.escalonador.tarefas_prontas)
        tarefas_em_espera.remove(processador)

        # Desenha tarefas em espera
        for tarefa in tarefas_em_espera:
            self.ax.broken_barh([(tempo_atual - 1, 1)], (tarefa.id * 1 - 0.3, 0.6), facecolors="white", edgecolors="black")

        # Desenha tarefa no processador
        self.ax.broken_barh([(tempo_atual - 1, 1)], (processador.id * 1 - 0.3, 0.6), facecolors=processador.cor, edgecolors="black")   

        # Ajusta o gráfico
        self.ax.set_xlim(0, tempo_atual)
        self.ax.set_xticks(range(0, tempo_atual + 1))
        self.canvas.draw()

    # Atualiza o quadro de informações da simulação passo a passo em tempo real
    def atualizar_info_simulacao(self):
        string_tarefas = ""
        for tarefa in self.escalonador.tarefas:
            string_tarefas += f"Tarefa {tarefa.id}; Ingresso: {tarefa.ingresso}; Duração Restante: {tarefa.duracao}; Prioridade: {tarefa.prioridade}\n"

        self.var_info_simulacao.set(
            f"Relógio: {self.escalonador.tempo}\n" +
            f"Tipo Escalonador: {self.escalonador.tipo}\n" + 
            f"Quantum restante: {self.escalonador.quantum_restante}\n" +
            string_tarefas
        )