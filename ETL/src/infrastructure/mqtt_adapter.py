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
        
        # AJUSTE AQUI: Declarando a versão da API para compatibilidade com o paho-mqtt 2.x
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        # Imprime o código de retorno para ajudar no debug se algo falhar
        print(f"Conectado ao Broker MQTT (Código: {rc}). Assinando tópico: {self.topic}")
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
        print(f"Tentando conectar no broker {self.broker} na porta {self.port}...")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()