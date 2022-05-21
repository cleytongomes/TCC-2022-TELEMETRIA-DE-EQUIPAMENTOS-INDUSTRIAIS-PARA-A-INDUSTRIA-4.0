#include <WiFi.h>
#include <PubSubClient.h>

// CONFIGURAÇÃO DO WI-FI
const char* ssid = "********";
const char* password = "*********";

const char* server_mqtt = "127.0.0.1";
const int port_mqtt = 8081;

const char* id_mqtt = "ID";
const char* user_mqtt = "admin";
const char* password_mqtt = "123456";
const char* topico_mqtt = "USINAGEM/MAQ01";

// PINO DO SENSOR INFRAVERMELHO
const int pin_d_sensor_infra = 8;
const int delay_mensagens = 30000; // 30 segundos

/* ESTADO MAQUINA
 *  true => ligada
 *  false => desligada
*/
boolean estado_maquina = false;
unsigned long ultima_transicao = 0;
const int delay_conf_desligamento = 300000; // 5 minutos


unsigned long ultima_mensagem = 0;
char mensagem[25];

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  // DEFINE O PINO COMO ENTRADA
  pinMode(pin_d_sensor_infra, INPUT);

  // ALTERA A VELOCIDADE DA SERIAL
  Serial.begin(115200);

  // CONFIGURA O WI-FI
  setup_wifi();

  // MONITORA O PINO DE ENTRADA
  attachInterrupt(digitalPinToInterrupt(pin_d_sensor_infra), muda_estado, CHANGE);

  client.setServer(server_mqtt, port_mqtt);
}

void loop() {

  // VERIFICA A CONEXÃO COM O BROKER
  if (!client.connected()) {
    reconnect();
  }

  // INICIA O LOOP
  client.loop();

  // TEMPO ATUAL
  unsigned long agora = millis();

  // VERIFICA SE A MÁQUINA ESTÁ DESLIGADA
  if (agora - ultima_transicao > delay_conf_desligamento) {
    estado_maquina = false;
    ultima_transicao = millis();
  }

  // ENVIA NOVA MENSAGEM PARA O BROKER
  if (agora - ultima_mensagem > delay_mensagens) {
    ultima_mensagem = agora;

    if (estado_maquina)
      snprintf (mensagem, 25, "{\"ESTADO\": \"EM TRABALHO\"}");
    else
      snprintf (mensagem, 25, "{\"ESTADO\": \"PARADA\"}");
    
    Serial.print("Mensagem: ");
    Serial.println(mensagem);

    // PUBLICA A MENSAGEM NO TÓPICO
    client.publish(topico_mqtt, mensagem);
  }
}
