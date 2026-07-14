from infrastructure.repositories import MySQLTelemetriaRepository
from application.use_cases import ProcessarLeituraUseCase
from infrastructure.mqtt_adapter import MqttConsumer

if __name__ == "__main__":
    # 1. Configurações
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'mysql',
        'database': 'agro_telemetria'
    }
    
    # 2. Instancia as dependências de Infraestrutura
    repositorio_mysql = MySQLTelemetriaRepository(db_config)
    
    # 3. Instancia a Aplicação injetando a Infraestrutura
    caso_de_uso = ProcessarLeituraUseCase(repository=repositorio_mysql)
    
    # 4. Inicia o Consumidor (Interface Externa)
    consumidor_mqtt = MqttConsumer(
        broker="localhost",
        port=1883,
        topic="fazenda/soja/telemetria",
        use_case=caso_de_uso
    )
    
    print("Iniciando Pipeline de Telemetria com DDD...")
    consumidor_mqtt.iniciar()