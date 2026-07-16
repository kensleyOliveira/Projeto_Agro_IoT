import os
import sys
from infrastructure.repositories import MySQLTelemetriaRepository
from application.use_cases import ProcessarLeituraUseCase
from infrastructure.mqtt_adapter import MqttConsumer

if __name__ == "__main__":
    print("==================================================")
    print("🚀 Iniciando Pipeline de Telemetria com DDD (AgroStock)")
    print("==================================================")

        
    db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3309)),  
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'mysql'),
            'database': os.getenv('DB_NAME', 'agro_telemetria'),
            'autocommit': True  
        }
    
    mqtt_broker = os.getenv('MQTT_BROKER', 'localhost')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    mqtt_topic = os.getenv('MQTT_TOPIC', 'kensley/fazenda/soja/telemetria')
    
    print(f"📡 Conectando ao MQTT Broker: {mqtt_broker}:{mqtt_port} no tópico '{mqtt_topic}'")
    print(f"🛢️ Target Database: {db_config['host']}:{db_config['port']} | DB: {db_config['database']}")

    try:
        # 2. Instancia as dependências de Infraestrutura
        repositorio_mysql = MySQLTelemetriaRepository(db_config)
        
        # 3. Instancia a Camada de Aplicação injetando a Infraestrutura (Inversão de Dependência)
        caso_de_uso = ProcessarLeituraUseCase(repository=repositorio_mysql)
        
        # 4. Inicia o Consumidor (Adaptador de Interface Externa)
        consumidor_mqtt = MqttConsumer(
            broker=mqtt_broker,
            port=mqtt_port,
            topic=mqtt_topic,
            use_case=caso_de_uso
        )
        
        print("🟢 Pipeline pronto para receber dados da ESP32. Escutando...")
        print("--------------------------------------------------")
        consumidor_mqtt.iniciar()

    except KeyboardInterrupt:
        print("\n🛑 Encerrando o Pipeline de Telemetria graciosamente...")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Erro crítico na inicialização do sistema: {e}")
        sys.exit(1)