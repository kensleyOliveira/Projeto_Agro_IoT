import os
from infrastructure.repositories import MySQLTelemetriaRepository
from application.use_cases import ProcessarLeituraUseCase
from infrastructure.mqtt_adapter import MqttConsumer

if __name__ == "__main__":
    print("Iniciando Pipeline de Telemetria com DDD...")

    # 1. Configurações Dinâmicas (Lê do Docker se existir, senão usa o padrão local)
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'mysql'),
        'database': os.getenv('DB_NAME', 'agro_telemetria')
    }
    
    mqtt_broker = os.getenv('MQTT_BROKER', 'localhost')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    mqtt_topic = os.getenv('MQTT_TOPIC', 'kensley/fazenda/soja/telemetria')
    
    # 2. Instancia as dependências de Infraestrutura
    repositorio_mysql = MySQLTelemetriaRepository(db_config)
    
    # 3. Instancia a Aplicação injetando a Infraestrutura
    caso_de_uso = ProcessarLeituraUseCase(repository=repositorio_mysql)
    
    # 4. Inicia o Consumidor (Interface Externa)
    consumidor_mqtt = MqttConsumer(
        broker=mqtt_broker,
        port=mqtt_port,
        topic=mqtt_topic,
        use_case=caso_de_uso
    )
    
    consumidor_mqtt.iniciar()