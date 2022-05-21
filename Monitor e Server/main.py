# Cliente MQtt para coletar informações das máquinas
# Autor: Cleyton Gomes
# Data: 12/04/2022
#
# Objetivo:
#   - Criar um cliente MQTT para coletar informações das máquinas
#   - Armazenar as informações em um banco de dados
#

from conector import ConectorBd
from maquina import Maquina
from broker import BrokerConnection

# Retorna um dicionário com as máquinas monitoradas
def maquinas_monitoradas():

    # Dicionário com as máquinas monitoradas
    maquinas_monitoradas = {}

    bd = ConectorBd()
    ult_historico_maquinas = bd.obter_estados()

    for ult_hs in ult_historico_maquinas:

        # Histórico finalizado
        finalizado = ult_hs[4]

        if finalizado:
            maquinas_monitoradas[ult_hs[1]] = Maquina(ult_hs[2], ult_hs[1], "Desconhecido")
        else:
            maquinas_monitoradas[ult_hs[1]] = Maquina(ult_hs[2], ult_hs[1], ult_hs[3])

    return maquinas_monitoradas


if __name__ == "__main__":

    maquinas = maquinas_monitoradas()
    broker = BrokerConnection(maquinas)



