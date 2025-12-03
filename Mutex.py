class Mutex:
    def __init__(self, id):
        self.id = int(id)
        self.isLocked = False
        self.tarefa = None