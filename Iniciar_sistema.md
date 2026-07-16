Aqui está um guia passo a passo completo estruturado em formato Markdown (`.md`).

Ele foi desenhado especificamente para o seu ecossistema IoT, detalhando de forma clara e profissional como iniciar e testar o sistema de ponta a ponta. Você pode copiar esse conteúdo, criar um arquivo chamado `README.md` na raiz do seu projeto e utilizá-lo inclusive para apresentar ao seu professor na UFU!

---

```markdown
# 🌾 Ecossistema IoT de Telemetria de Microclima - AgroStock

Este repositório contém a infraestrutura e os sistemas para o monitoramento hiperlocal de temperatura e umidade em lavouras e armazenamento de insumos. O sistema opera sob uma arquitetura orientada a eventos e Domain-Driven Design (DDD).

---

## 🏗️ Visão Geral da Arquitetura

O fluxo de dados do ecossistema funciona de forma totalmente automatizada:
1. **Borda (Sensor):** O microcontrolador ESP32 realiza a leitura física de temperatura e umidade com o sensor DHT22.
2. **Mensageria (Broker):** Os dados são publicados em tópicos de um Broker MQTT (HiveMQ / Mosquitto).
3. **Ingestão (ETL):** Um serviço de ETL em Python (empacotado via Docker) consome os eventos do Broker, valida e persiste no banco de dados.
4. **Banco de Dados:** MySQL persistente (rodando em contêiner Docker na porta `3309`).
5. **Backend/Painel (Next.js):** API e Dashboard em tempo real consumindo os dados diretamente do banco de dados.
6. **Mobile (Android/Kotlin):** Aplicativo móvel que consome a API do Next.js para exibição das telemetrias na palma da mão.

---

## 🚀 Guia Passo a Passo para Rodar o Sistema Completo

### 📋 Pré-requisitos
Certifique-se de ter instalado em sua máquina de desenvolvimento:
* **Docker e Docker Compose** (Docker Desktop instalado e ativo)
* **Node.js** (v18 ou superior para rodar o Next.js)
* **Android Studio** (para compilar e instalar o app mobile no celular)

---

### 🐳 Passo 1: Subir o Banco de Dados e o ETL (Docker)

O banco de dados MySQL e o serviço de ETL estão totalmente conteinerizados. Para subir esses serviços de forma isolada e sem conflito de portas no Windows:

1. Abra o terminal (Prompt de Comando, PowerShell ou Terminal do VS Code) na raiz do seu projeto (onde está o arquivo `docker-compose.yml`).
2. Execute o comando para baixar/compilar as imagens e subir os contêineres em segundo plano:
   ```bash
   docker compose up -d

```

3. Verifique se os dois contêineres estão rodando normalmente:
```bash
docker ps

```


*Você deverá ver os contêineres `agro_mysql_container` (porta `3309`) e `agro_etl_container` ativos.*

---

### 🌐 Passo 2: Configurar e Rodar o Backend (Next.js)

O Next.js atuará como o servidor de API central para a aplicação Web e o aplicativo Android.

1. Navegue até a pasta do seu projeto frontend/backend:
```bash
cd Backend/agro_backend

```


2. Caso seja a primeira execução, instale as dependências do projeto:
```bash
npm install

```


3. **Descubra o IP local do seu computador:**
Antes de rodar, precisamos do IP do seu notebook para que o celular Android na mesma rede consiga acessá-lo. No terminal, execute:
* **No Windows:** `ipconfig` (procure pelo IP IPv4 da sua placa de rede Ethernet ou Wi-Fi ativa. Exemplo: `192.168.1.110`).


4. **Inicie o servidor de desenvolvimento do Next.js** forçando o bind no seu IP local:
```bash
npx next dev -H 192.168.1.110

```


*(Substitua `192.168.1.110` pelo IP real que você obteve no passo anterior).*
5. **Acesse a Plataforma Web:**
Abra seu navegador e acesse: `http://192.168.1.110:3000`. O painel institucional e o gráfico de monitoramento histórico devem carregar com os horários sincronizados perfeitamente!

---

### 📱 Passo 3: Configurar e Rodar o Aplicativo Android (Kotlin)

Para que o aplicativo instalado no smartphone se comunique com a API hospedada no seu computador, eles precisam estar na **mesma rede local** (ex: conectados no mesmo Wi-Fi).

1. Abra o projeto do aplicativo Android no **Android Studio**.
2. No arquivo de configuração ou classe de serviço de rede (onde está a declaração do Retrofit ou Ktor), localize a constante de URL Base.
3. Atualize a URL com o IP obtido no passo anterior e a porta do Next.js (`3000`):
```kotlin
// Altere para o IP atual do seu notebook na rede
val BASE_URL = "[http://192.168.1.110:3000/api/](http://192.168.1.110:3000/api/)"

```


4. Conecte seu dispositivo físico Android via USB, ative a Depuração USB e clique no botão **Run** (`Shift + F10`) no Android Studio para instalar o app no celular.

---

## 📝 Resumo de Comandos Rápidos

| Serviço | Diretório | Comando | Detalhes |
| --- | --- | --- | --- |
| **Banco & ETL** | Raiz do Projeto | `docker compose up -d` | Sobe o MySQL na porta `3309` e o ETL |
| **Backend API** | `Backend/agro_backend` | `npx next dev -H <seu_ip_local>` | Expõe o painel web e API para a rede local |
| **Mobile App** | Android Studio | `Run (Shift + F10)` | Compila e envia o app para o celular |

---

## 💡 Dica para o Dia da Apresentação na UFU

Ao chegar na faculdade e se conectar à rede Wi-Fi da UFU ou ancorar no ponto de acesso do celular, **o seu endereço IP vai mudar**.

Para colocar o sistema no ar de forma rápida:

1. Abra o terminal e rode `ipconfig` para ver o novo IP.
2. Atualize o `BASE_URL` no código do Android com este novo IP e recompile o app.
3. Inicie o Next.js apontando para este novo IP: `npx next dev -H <novo_ip_local>`.

```

```