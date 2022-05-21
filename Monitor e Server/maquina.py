import time
from conector import ConectorBd

class Maquina:
    def __init__(self, nome, id, estado):
        self.nome = nome
        self.id = id
        self.estado = estado
        self.ultima_atividade = time.strftime("%Y-%m-%d %H:%M:%S")

    def atualizar_estado(self, valor_estado):
        if valor_estado != self.estado:   
            self.estado = valor_estado
            self.__atualiza_estado_banco_de_dados(valor_estado)

        self.ultima_atividade = time.time()

    def __atualiza_estado_banco_de_dados(self, estado):
        bd = ConectorBd()
        bd.atualiza_estado_maquina(self.id, self.estado)