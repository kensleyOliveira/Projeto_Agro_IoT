#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// ====================================================================
// CONFIGURAÇÕES DE REDE E SERVIDOR
// ====================================================================
const char* ssid        = "MegaWiFiAna Paula";       // Substitua pelo nome do seu Wi-Fi residencial
const char* password    = "apff1974";               // Substitua pela senha do seu Wi-Fi residencial
const char* mqtt_server = "broker.hivemq.com";       // Broker Público HiveMQ na Nuvem
const int mqtt_port      = 1883;                     // Porta padrão do MQTT

// Tópico altamente específico para evitar interferência de terceiros no Broker Público
const char* mqtt_topic = "kensley/fazenda/soja/telemetria";

// ====================================================================
// CONFIGURAÇÕES DO SENSOR DHT22
// ====================================================================
#define DHTPIN 14          // GPIO 14 (Pino seguro que evita travamentos no boot da ESP32)
#define DHTTYPE DHT22      // Definindo o modelo do sensor
DHT dht(DHTPIN, DHTTYPE);

// Instanciação dos clientes de rede e MQTT
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long ultimoEnvio = 0;

// ====================================================================
// FUNÇÃO DE CONEXÃO WI-FI
// ====================================================================
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se a: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado com sucesso!");
  Serial.print("Endereço IP da ESP32: ");
  Serial.println(WiFi.localIP());
}

// ====================================================================
// FUNÇÃO DE CONEXÃO/RECONEXÃO AO BROKER MQTT (NUVEM)
// ====================================================================
void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao Broker HiveMQ Cloud...");
    
    // Gera um ID de cliente único para evitar que sua ESP seja desconectada por clones
    String clientId = "ESP32_Soja_Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println(" conectado com sucesso!");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      Serial.println(". Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

// ====================================================================
// CONFIGURAÇÃO INICIAL (SETUP)
// ====================================================================
void setup() {
  Serial.begin(115200);
  
  // Inicializa o sensor físico
  dht.begin();
  
  // Conecta ao Wi-Fi local
  setup_wifi();
  
  // Configura os dados do servidor MQTT
  client.setServer(mqtt_server, mqtt_port);
}

// ====================================================================
// LAÇO PRINCIPAL (LOOP)
// ====================================================================
void loop() {
  // Garante que a ESP32 permaneça sempre conectada ao HiveMQ
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Executa a leitura e envio a cada 10 segundos
  unsigned long agora = millis();
  if (agora - ultimoEnvio > 10000) {
    ultimoEnvio = agora;

    float umidade = dht.readHumidity();
    float temperatura = dht.readTemperature();

    // Valida se a leitura física do sensor foi bem-sucedida
    if (isnan(umidade) || isnan(temperatura)) {
      Serial.println("Erro: Falha ao ler dados do sensor DHT22!");
      return;
    }

    // Monta o payload padronizado em JSON comercial
    String payload = "{";
    payload += "\"sensor_id\":\"ESP32_BLOCO_A\",";
    payload += "\"temperatura\":" + String(temperatura, 1) + ",";
    payload += "\"umidade\":" + String(umidade, 1);
    payload += "}";

    Serial.print("Enviando para o HiveMQ -> ");
    Serial.println(payload);
    
    // Publica a mensagem no tópico monitorado pelo backend
    client.publish(mqtt_topic, payload.c_str());
  }
}