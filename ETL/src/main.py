import os
import sys
from infrastructure.repositories import PostgresTelemetriaRepository
from application.use_cases import ProcessarLeituraUseCase
from infrastructure.mqtt_adapter import MqttConsumer

if __name__ == "__main__":
    print("==================================================")
    print("🚀 Iniciando Pipeline Cloud-Native com DDD (AgroStock)")
    print("==================================================")
        
    db_config = {
        'host': os.getenv('DB_HOST', 'aws-0-sa-east-1.pooler.supabase.com'), 
        'port': int(os.getenv('DB_PORT', 6543)), 
        'user': os.getenv('DB_USER', 'postgres.bubejagemuavlpkmiabc'),  
        'password': os.getenv('DB_PASSWORD', 'UE5S8DxTTAKpudhc'), 
        'database': os.getenv('DB_NAME', 'postgres')  
    }

    mqtt_broker = os.getenv('MQTT_BROKER', '16faa5db8a444e2188dc03acb0032661.s1.eu.hivemq.cloud')
    mqtt_port = int(os.getenv('MQTT_PORT', 8883)) 
    mqtt_user = os.getenv('MQTT_USER', 'agro_worker')
    mqtt_password = os.getenv('MQTT_PASSWORD', 'Jatoba@1972')
    mqtt_topic = os.getenv('MQTT_TOPIC', 'kensley/fazenda/soja/telemetria')
    
    print(f"📡 Target Broker: {mqtt_broker}:{mqtt_port} | Tópico: '{mqtt_topic}'")
    print(f"🛢️ Target Database Cloud: {db_config['host']} | DB: {db_config['database']}")

    try:
        repositorio_postgres = PostgresTelemetriaRepository(db_config)
        
        caso_de_uso = ProcessarLeituraUseCase(repository=repositorio_postgres)

        consumidor_mqtt = MqttConsumer(
            broker=mqtt_broker,
            port=mqtt_port,
            topic=mqtt_topic,
            user=mqtt_user,
            password=mqtt_password,
            use_case=caso_de_uso
        )
        
        print("🟢 Pipeline em nuvem pronto e escutando a ESP32...")
        print("--------------------------------------------------")
        consumidor_mqtt.iniciar()

    except KeyboardInterrupt:
        print("\n🛑 Encerrando o Pipeline de Telemetria graciosamente...")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Erro crítico na inicialização do sistema: {e}")
        sys.exit(1)