@echo off
title Orquestrador Agro_IoT
echo =======================================================
echo           INICIANDO ECOSSISTEMA AGRO_IOT
echo =======================================================

:: 1. Iniciar o Broker Mosquitto usando o caminho absoluto com aspas
echo [1/4] Inicializando Broker Mosquitto...
start /b "" "C:\Program Files\Mosquitto\mosquitto.exe" -c "C:\Program Files\Mosquitto\agro.conf"

:: 2. Garantir que o serviço do MySQL está rodando
echo [2/4] Verificando Servico MySQL...
net start MySQL80 >nul 2>&1

:: 3. Aguardar 3 segundos para estabilização da rede local
timeout /t 3 /nobreak >nul

:: 4. Iniciar o ETL Python em uma janela separada (minimizado)
echo [3/4] Inicializando Pipeline ETL Python (DDD)...
cd /d "E:\USUARIO\37_Sistema_de_Informacao\curso\5o_Semestre\Programacao_Dispositivo_Moveis\Trabalho\Codigo\ETL"
start /min cmd /k "python src/main.py"

:: 5. Iniciar o Servidor Next.js (Backend/API) em modo dev
echo [4/4] Inicializando Servidor Next.js (Porta 3000)...
cd /d "E:\USUARIO\37_Sistema_de_Informacao\curso\5o_Semestre\Programacao_Dispositivo_Moveis\Trabalho\Codigo\Backend\agro_backend"
start /min cmd /k "npm run dev"

echo =======================================================
echo    SISTEMA AGRO_IOT RODANDO COM SUCESSO EM SEGUNDO PLANO!
echo    - MQTT: Porta 1883
echo    - Next.js API: http://localhost:3000
echo    - Pressione qualquer tecla para fechar esta janela.
echo =======================================================
pause