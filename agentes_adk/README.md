# Sistema Multi-Agente com Google ADK

Este diretório contém uma implementação de sistema de agentes inteligentes utilizando o Google Agent Development Kit (ADK), demonstrando diferentes abordagens para criação de chatbots e assistentes virtuais.

## 📋 Visão Geral

O diretório está organizado na principal implementação:

1. **`agente_implementacao/`** - Sistema completo multi-agente com orquestração

## 🏗 Estrutura do Projeto

```
agentes_adk/
├── agente_implementacao/            # Sistema completo
│   ├── agents/                      # Agentes especializados
│   │   ├── agente_bigquery.py      # Agente para consultas SQL
│   │   └── agente_sauter.py        # Agente para busca web
│   ├── ferramentas/                 # Ferramentas personalizadas
│   │   ├── bigquery_busca_ferramenta.py
│   │   └── sauter_busca_tool.py
│   ├── orquestrador/                # Sistema de orquestração
│   │   └── orquestrador.py         # Agente coordenador
│   ├── runner.py                    # API FastAPI
│   └── README.md                    # Documentação detalhada
└── README.md                        # Esta documentação
```

## 🛠 Pré-requisitos

### Software Necessário
- **Python 3.10+**
- **Google Cloud CLI** configurado
- **Conta Google Cloud** com faturamento ativado

### Instalação de Dependências
```bash
# Clone o repositório (se necessário)
cd api

# Crie e ative um ambiente virtual (opcional com UV)
python -m venv venv

source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows]

# Instalar o Google ADK
pip install google-adk

# Outras dependências essenciais
pip install google-generativeai google-cloud-bigquery fastapi uvicorn python-dotenv
```

### Configuração do Ambiente
```bash
# Configurar variáveis de ambiente
export GOOGLE_GENAI_USE_VERTEXAI="True" #False para uso sem cobranças
export GOOGLE_CLOUD_PROJECT="seu-projeto-gcp"
export GOOGLE_CLOUD_LOCATION="us-central1" #Região mais barata para o Brasil atualmente
```

## 🚀 Como Usar

### Exemplo 1: Multi-Tool Agent (Básico)

Este exemplo demonstra um agente simples com ferramentas para consultar tempo e clima.

```bash
# Navegar para o diretório
cd agentes_adk/adk_estudo

# Executar o agente
python -c "
from multi_tool_agent.agent import root_agent
from google.adk.runners import Runner

runner = Runner(agent=root_agent, app_name='weather_app')
# Use o runner para interagir com o agente
"
```

**Funcionalidades:**
- ✅ Consulta de clima para Nova York
- ✅ Consulta de horário atual para Nova York
- ✅ Respostas estruturadas com status e mensagens

### Exemplo 2: Sistema Multi-Agente (Avançado)

Sistema completo com orquestração inteligente e múltiplos agentes especializados.

#### Configuração Inicial

1. **Configurar variáveis de ambiente**:
```bash
# Criar arquivo .env
cd agentes_adk/agente_implementacao

cat > .env << EOF
GOOGLE_CLOUD_PROJECT=seu-projeto-gcp
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_SEARCH_API_KEY=sua-api-key-google
GOOGLE_SEARCH_ENGINE_ID=seu-engine-id
EOF
```

2. **Configurar BigQuery**:
   - Crie uma tabela no BigQuery com dados de empresas
   - Configure as credenciais de acesso

#### Execução da API

```bash
# Instalar dependências específicas
pip install fastapi uvicorn google-cloud-bigquery googleapiclient-discovery-py3

# Executar a API
cd agentes_adk/agente_implementacao
python runner.py

# Ou usar uvicorn diretamente
uvicorn runner:app --host 0.0.0.0 --port 8000 --reload
```

#### Testando a API

```bash
# Teste básico
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quais são os serviços da Sauter?",
    "user_id": "user123",
    "session_id": "session456"
  }'

# Consulta sobre dados de empresas
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quantas empresas têm mais de 100 funcionários?",
    "user_id": "user123",
    "session_id": "session456"
  }'
```

## 🤖 Agentes Disponíveis

### 1. Orquestrador (`orchestrator_agent`)
**Função**: Analisa perguntas e delega para agentes especializados
- Não responde diretamente às perguntas
- Roteia inteligentemente entre agentes
- Usa o modelo `gemini-2.0-flash`

### 2. Agente Sauter (`sauter_agent`)  
**Função**: Especialista em informações da empresa Sauter
- Realiza buscas no site `sauter.digital`
- Usa Google Custom Search API
- Fornece informações atualizadas sobre serviços e empresa

# NÃO TESTADO
### 3. Agente BigQuery (`bigquery_agent`)
**Função**: Analista de dados especializado em SQL
- Converte perguntas em consultas SQL
- Executa queries no Google BigQuery
- Analisa dados de empresas de consultoria

## 🛡️ Ferramentas Customizadas

### BigQuery Tool
```python
# Exemplo de uso da ferramenta
from ferramentas.bigquery_busca_ferramenta import run_bigquery_sql_tool

# Executa consulta SQL automaticamente
resultado = run_bigquery_sql_tool("SELECT COUNT(*) FROM empresas")
```

### Google Search Tool
```python
# Busca específica no site sauter.digital
from ferramentas.sauter_busca_tool import perform_google_site_search

resultados = perform_google_site_search("serviços digitais")
```

## 📊 API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/chat` | POST | Enviar mensagem para o sistema multi-agente |
| `/` | GET | Status da API |
| `/docs` | GET | Documentação automática (Swagger UI) |

### Exemplo de Request/Response

**Request:**
```json
{
  "query": "Qual o faturamento médio das empresas?",
  "user_id": "user123",
  "session_id": "session456"
}
```

**Response:**
```json
{
  "response": "Com base nos dados analisados, o faturamento médio das empresas é de R$ 2.5 milhões...",
  "user_id": "user123",  
  "session_id": "session456"
}
```

## 🔧 Configurações Avançadas

### Logging e Debug
```python
import logging

# Configurar logs detalhados
logging.basicConfig(level=logging.INFO)

# Para debug do ADK
os.environ["ADK_DEBUG"] = "true"
```

### Sessões Personalizadas
```python
from google.adk.sessions import InMemorySessionService

# Usar serviço de sessão customizado
session_service = InMemorySessionService()
runner = Runner(
    agent=orchestrator_agent,
    app_name="meu_app",
    session_service=session_service
)
```

## 📈 Monitoramento e Logs

- Logs automáticos das interações entre agentes
- Rastreamento de queries SQL executadas
- Monitoramento de buscas web realizadas
- Métricas de performance das APIs

## 🚨 Solução de Problemas

### Problemas Comuns

1. **Erro de Autenticação Google Cloud**
   ```bash
   gcloud auth application-default login
   ```

2. **Problemas com BigQuery**
   - Verificar permissões da Service Account
   - Confirmar se a tabela existe e tem dados

3. **API de Busca não funciona**
   - Verificar se `GOOGLE_SEARCH_API_KEY` está configurada
   - Confirmar cotas da API de busca customizada

4. **Agente não responde**
   - Verificar logs do console
   - Confirmar se o modelo Gemini está disponível

### Debug Avançado

```bash
# Logs detalhados
export ADK_DEBUG=true
export TF_LOG=DEBUG

# Executar com logs verbosos
python runner.py --log-level DEBUG
```

## 📝 Desenvolvimento

### Adicionando Novos Agentes

1. Criar novo arquivo em `agents/`
2. Implementar ferramentas necessárias em `ferramentas/`
3. Registrar no orquestrador
4. Atualizar instruções de roteamento

### Exemplo de Novo Agente
```python
from google.adk.agents import Agent

novo_agente = Agent(
    name="meu_agente",
    model="gemini-2.0-flash", 
    description="Descrição do agente",
    instruction="Instruções detalhadas...",
    tools=[minhas_ferramentas]
)
```

## 📞 Suporte

Para mais informações:
- 📖 [Documentação do Google ADK](https://cloud.google.com/vertex-ai/docs/agent-builder)
- 🛠 [Google Cloud Console](https://console.cloud.google.com)
- 📧 Verifique os logs da aplicação para debugging detalhado

## 🎯 Próximos Passos

1. Implementar cache para consultas frequentes
2. Adicionar autenticação e autorização
3. Criar dashboards de monitoramento
4. Expandir base de conhecimento dos agentes
5. Implementar testes automatizados