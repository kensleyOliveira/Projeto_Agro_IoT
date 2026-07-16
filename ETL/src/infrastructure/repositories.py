import time
import mysql.connector
from domain.models import LeituraMicroclima
from application.interfaces import ITelemetriaRepository

class MySQLTelemetriaRepository(ITelemetriaRepository):
       
    def __init__(self, db_config: dict):
        self.config = db_config

    def salvar(self, leitura: LeituraMicroclima) -> None:
        conexao = None
        tentativas = 5
        intervalo = 3 
        
        for tentativa in range(tentativas):
            try:
                conexao = mysql.connector.connect(**self.config)
                cursor = conexao.cursor()
                
                sql = "INSERT INTO telemetria_microclima (temperatura, umidade, timestamp) VALUES (%s, %s, %s)"
                valores = (leitura.temperatura, leitura.umidade, leitura.timestamp)
                
                cursor.execute(sql, valores)
                conexao.commit()
                break
                
            except mysql.connector.Error as err:
                print(f"Tentativa {tentativa + 1}/{tentativas} falhou. Banco pode estar inicializando...")
                if tentativa == tentativas - 1:
                    print(f"Erro definitivo de Infraestrutura (MySQL): {err}")
                    raise err
                time.sleep(intervalo) 
                
            finally:
                if conexao and conexao.is_connected():
                    cursor.close()
                    conexao.close()