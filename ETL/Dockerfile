FROM python:3.10-slim

WORKDIR /app

# Copia os requisitos e instala as bibliotecas (paho-mqtt, mysql-connector-python)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da camada SRC para dentro do contêiner
COPY src/ ./src/

# Executa o main.py
CMD ["python", "src/main.py"]