import mysql.connector
from domain.models import LeituraMicroclima
from application.interfaces import ITelemetriaRepository

class MySQLTelemetriaRepository(ITelemetriaRepository):
       
    def __init__(self, db_config: dict):
        self.config = db_config

    def salvar(self, leitura: LeituraMicroclima) -> None:
        conexao = None
        try:
            conexao = mysql.connector.connect(**self.config)
            cursor = conexao.cursor()
            
            sql = "INSERT INTO telemetria_microclima (temperatura, umidade, timestamp) VALUES (%s, %s, %s)"
            valores = (leitura.temperatura, leitura.umidade, leitura.timestamp)
            
            cursor.execute(sql, valores)
            conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro de Infraestrutura (MySQL): {err}")
            raise err
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()