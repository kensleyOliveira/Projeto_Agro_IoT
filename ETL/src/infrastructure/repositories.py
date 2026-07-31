import time
import psycopg2
from domain.models import LeituraMicroclima
from application.interfaces import ITelemetriaRepository

class PostgresTelemetriaRepository(ITelemetriaRepository):
       
    def __init__(self, db_config: dict):
        self.config = db_config

    def salvar(self, leitura: LeituraMicroclima) -> None:
        conexao = None
        tentativas = 5
        intervalo = 3 
        
        for tentativa in range(tentativas):
            try:
                # Conecta ao PostgreSQL do Supabase
                conexao = psycopg2.connect(**self.config)
                cursor = conexao.cursor()
                
                # Query adaptada com sintaxe padrão ANSI/Postgres
                sql = """
                    INSERT INTO telemetria_microclima (temperatura, umidade, timestamp) 
                    VALUES (%s, %s, %s);
                """
                valores = (leitura.temperatura, leitura.umidade, leitura.timestamp)
                
                cursor.execute(sql, valores)
                conexao.commit()
                cursor.close()
                break
                
            except Exception as err:
                print(f"⚠️ [Infra] Tentativa {tentativa + 1}/{tentativas} falhou ao conectar ao Supabase...")
                if tentativa == tentativas - 1:
                    print(f"❌ Erro definitivo de Infraestrutura (PostgreSQL): {err}")
                    raise err
                time.sleep(intervalo) 
                
            finally:
                if conexao:
                    conexao.close()