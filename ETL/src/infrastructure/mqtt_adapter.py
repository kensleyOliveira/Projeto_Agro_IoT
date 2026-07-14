import json
import paho.mqtt.client as mqtt
from application.use_cases import ProcessarLeituraUseCase

class MqttConsumer:
    """Consumidor MQTT que atua como porta de entrada (Driver) para o sistema"""
    
    def __init__(self, broker: str, port: int, topic: str, use_case: ProcessarLeituraUseCase):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.use_case = use_case
        
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao Broker MQTT. Assinando tópico: {self.topic}")
        client.subscribe(self.topic)

    def _on_message(self, client, userdata, msg):
        try:
            # Extrai o payload JSON
            payload = json.loads(msg.payload.decode('utf-8'))
            
            # Delega a responsabilidade para a camada de Aplicação
            self.use_case.executar(payload)
            
        except json.JSONDecodeError:
            print("Erro de Infraestrutura: Falha ao decodificar JSON.")

    def iniciar(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()