import mysql.connector
import configparser
import time

class ConectorBd:

    def __init__(self):
        
        config = configparser.ConfigParser()
        config.read('config.ini')

        config['MQTT']['BROKER']

        self.__host = config['BANCO DE DADOS']['HOST']
        self.__user = config['BANCO DE DADOS']['USUARIO']
        self.__senha = config['BANCO DE DADOS']['SENHA']
        self.__database = config['BANCO DE DADOS']['DATABASE']
        self.__port = int(config['BANCO DE DADOS']['PORTA'])
        
        try:
          self.__conexao = mysql.connector.connect(
                  host=self.__host,
                  user=self.__user,
                  password=self.__senha,
                  database=self.__database,
                  port=self.__port
              )
          self.__cursor = self.__conexao.cursor()

        except Exception as e:
            print("Erro ao conectar a base : ", e)


    def obter_estados(self):
        try:
            sql =   "SELECT hs.historico_id id, mq.maquina_id, mq.nome, hs.estado, IF(hs.fim, 1, 0) " \
                    "FROM maquinas mq " \
                    "left join historicos hs " \
                    "on mq.maquina_id = hs.cod_maquina " \
                    "where hs.historico_id IN (SELECT MAX(historico_id) FROM historicos GROUP BY cod_maquina ) " \
                    "order by mq.maquina_id" 

            self.__cursor.execute(sql)
            registros = self.__cursor.fetchall()

            return registros
        except Exception as e:
            print("Erro ao obter estados : ", e)


    def obter_maquinas(self):
        try:
            sql = "SELECT maquina_id, nome FROM maquinas"

            self.__cursor.execute(sql)
            registros = self.__cursor.fetchall()

            return registros
        except Exception as e:
            print("Erro ao obter maquinas : ", e)


    def obter_tempo_por_estado(self, cod_maquina):
        try:
            sql = "SELECT estado, sum(TIMESTAMPDIFF(HOUR, inicio, fim)) tempo FROM historicos WHERE cod_maquina = %s group by estado"
            valores = [cod_maquina]

            self.__cursor.execute(sql, valores)
            registros = self.__cursor.fetchall()

            return registros
        except Exception as e:
            print("Erro ao obter tempo por estado : ", e)


    def atualiza_estado_maquina(self, maquina_id, estado):
        self.finaliza_historico(maquina_id)
        self.insere_historico(maquina_id, estado)


    def insere_historico(self, maquina_id, estado):        
        try:
            sql = "INSERT INTO historicos (cod_maquina, estado, inicio) VALUES (%s, %s, %s)"
            valores = (maquina_id, estado, time.strftime('%Y-%m-%d %H:%M:%S'))

            self.__cursor.execute(sql, valores)
            self.__conexao.commit()

        except Exception as e:
            print("Erro ao inserir histórico : ", e)


    def finaliza_historico(self, maquina_id):
        try:
            sql = "UPDATE historicos SET fim = %s WHERE fim is null and cod_maquina = %s"
            valores = (time.strftime('%Y-%m-%d %H:%M:%S'), maquina_id)

            self.__cursor.execute(sql, valores)
            self.__conexao.commit()

        except Exception as e:
            print("Erro ao finalizar histórico : ", e)
    

    def finaliza_historicos_abertos(self):
        try:
            sql = "UPDATE historicos SET fim = %s WHERE fim is null"
            valores = [time.strftime('%Y-%m-%d %H:%M:%S')]

            self.__cursor.execute(sql, valores)
            self.__conexao.commit()

        except Exception as e:
            print("Erro ao finalizar históricos abertos : ", e)
