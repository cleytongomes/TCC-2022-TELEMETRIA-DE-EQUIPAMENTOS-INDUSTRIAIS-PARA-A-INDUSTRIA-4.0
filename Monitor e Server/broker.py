import paho.mqtt.client as mqtt
from conector import ConectorBd
import configparser
import logging
import json

class BrokerConnection:
    def __init__(self, maquinas_monitoradas):
        
        # Maquinas que serão monitoradas
        self.maquinas_monitoradas = maquinas_monitoradas

        # Configura o logging
        logging.basicConfig(filename='mqtt.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('INICIANDO CONEXÃO COM O BROKER')

        # Configurações do broker
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.__broker  = config['MQTT']['BROKER']
        self.__porta   = int(config['MQTT']['PORTA'])
        self.__usuario = config['MQTT']['USUARIO']
        self.__senha   = config['MQTT']['SENHA']

        self.id_cliente  = config['CLIENTE']['IDENTIFICADOR']
        self.topico      = config['CLIENTE']['TOPICO']

        self.cliente = mqtt.Client(self.id_cliente)
        self.cliente.on_connect = self.on_connect
        self.cliente.on_message = self.on_message
        self.cliente.on_disconnect = self.on_disconnect
        self.cliente.on_log = self.on_log

        self.cliente.username_pw_set(self.__usuario, self.__senha)
        self.cliente.connect(self.__broker, self.__porta)

        try:
            self.cliente.loop_forever()
        except KeyboardInterrupt:
            print("Finalizando.... ")
            self.cliente.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("Conexão realizada com sucesso")
        else:
            print(f"Conexão recusada codigo = {rc}")

        client.subscribe(self.topico) 

        
    def on_message(self, client, userdata, msg):
        print("mensagem recebida: topico => " + msg.topic + "; Mensagem => " + str(msg.payload))
        
        maquina = msg.topic.split('/')[1]
        
        mensagem = msg.payload.decode("utf-8")
        mensagem_json = json.loads(mensagem)

        estado = mensagem_json['estado']

        if maquina in self.maquinas_monitoradas:
            self.maquinas_monitoradas[maquina].atualizar_estado(estado)

    def on_disconnect(self, client, userdata, rc):
        print("Desconectado do Broker")

        bd = ConectorBd()
        bd.finaliza_historicos_abertos()
    
    def on_log(self, client, userdata, level, buf):
        logging.warning(buf)
