# Reservatórios API

Uma API FastAPI completa para gerenciar pipelines de dados de reservatórios da ONS (Operador Nacional do Sistema Elétrico) e consultar dados armazenados no Google BigQuery.

## 📋 Visão Geral

Esta API oferece três funcionalidades principais:

1. **Health Check**: Verificação do status da aplicação
2. **Pipeline Management**: Disparo e execução da pipeline ETL (Extract, Transform, Load)
3. **Data Querying**: Consulta de dados processados no BigQuery

A aplicação está estruturada seguindo as melhores práticas de desenvolvimento, com separação clara de responsabilidades entre routers, services, utils e pipeline.

## 🏗️ Arquitetura

```
api/
├── src/app/                    # Código principal da aplicação
│   ├── main.py                # Ponto de entrada da FastAPI
│   ├── pipeline_client.py     # Cliente para execução da pipeline
│   ├── routers/               # Endpoints da API
│   │   ├── health.py         # Health check
│   │   ├── pipeline.py       # Gerenciamento da pipeline
│   │   └── data.py           # Consulta de dados
│   ├── services/             # Serviços de negócio
│   │   └── bigquery_service.py # Integração com BigQuery
│   └── utils/                # Utilitários
│       └── logger.py         # Configuração de logging
├── pipeline/                 # Módulos ETL
│   ├── extract.py           # Extração de dados da API ONS
│   ├── transform.py         # Transformação e limpeza dos dados
│   └── load.py              # Carregamento no BigQuery/GCS
└── Dockerfile               # Container Docker
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- Google Cloud SDK configurado
- Credenciais do Google Cloud com acesso ao BigQuery
- UV (recomendado) ou pip para gerenciamento de dependências

### 1. Configuração do Ambiente

```bash
# Clone o repositório (se necessário)
cd api

# Crie e ative um ambiente virtual (opcional com UV)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
uv pip install -r src/app/requirements.txt
# ou
pip install -r src/app/requirements.txt
```

### 2. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto api com:

```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=seu-projeto-gcp
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# BigQuery
TABLE_ID=seu-projeto.dataset.tabela

# Storage (se usar GCS)
BUCKET_NAME=seu-bucket-gcs
```

### 3. Executar a Aplicação

#### Desenvolvimento Local

```bash
cd src/app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Produção

```bash
cd src/app
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Executar com Docker

```bash
# Build da imagem
docker build -t reservatorios-api .

# Executar o container
docker run -p 8000:8000 \
  -e GOOGLE_CLOUD_PROJECT=seu-projeto \
  -v /path/to/credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  reservatorios-api
```

## 📚 Endpoints da API

### Health Check
- **GET** `/api/v1/health/health`
- Verifica se a aplicação está funcionando

### Pipeline
- **POST** `/api/v1/pipeline/pipeline`
- Dispara a execução da pipeline ETL em background

### Dados
- **GET** `/api/v1/data/data`
- Consulta dados no BigQuery
- Parâmetros:
  - `limit`: Número máximo de registros (1-1000, padrão: 100)
  - `offset`: Número de registros a pular (padrão: 0)
  - `date`: Filtrar por data (formato: YYYY-MM-DD)

## 🔄 Pipeline ETL

A pipeline é composta por três etapas:

### 1. Extract (`pipeline/extract.py`)
- Conecta à API da ONS
- Baixa arquivos Parquet mais recentes por ano
- Salva localmente na pasta `downloads/`

### 2. Transform (`pipeline/transform.py`)
- Carrega arquivos Parquet
- Combina dados de diferentes anos
- Remove colunas desnecessárias
- Normaliza tipos de dados

### 3. Load (`pipeline/load.py`)
- Carrega dados transformados no BigQuery
- Opcional: backup no Google Cloud Storage

## 📖 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Deploy com Google Cloud Build

O projeto inclui configuração para deploy automático:

```bash
# Submit build para Google Cloud
gcloud builds submit --config cloudbuild.yaml .
```

## 🧪 Testes

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
pytest

# Executar com coverage
pytest --cov=src
```

## 📝 Logs

Os logs são configurados automaticamente e incluem:
- Informações de requisições HTTP
- Status da pipeline ETL
- Erros e exceções
- Consultas ao BigQuery

## ⚠️ Troubleshooting

### Problemas Comuns

1. **Erro de autenticação Google Cloud**
   - Verifique se `GOOGLE_APPLICATION_CREDENTIALS` aponta para arquivo válido
   - Confirme que a service account tem permissões necessárias

2. **Pipeline não executa**
   - Verifique logs em `/pipeline/logs/`
   - Confirme conectividade com API da ONS
   - Verifique espaço em disco para downloads

3. **Consultas BigQuery falham**
   - Confirme que a tabela existe no BigQuery
   - Verifique permissões da service account
   - Valide formato do `TABLE_ID`

### Comandos Úteis

```bash
# Verificar logs da aplicação
tail -f pipeline/logs/app.log

# Testar conectividade com BigQuery
python -c "from google.cloud import bigquery; print(bigquery.Client().list_datasets())"

# Verificar arquivos baixados
ls -la downloads/
```

## 🔧 Configuração Avançada

### Customização da Pipeline

Para modificar a pipeline, edite os arquivos em `pipeline/`:
- `extract.py`: Alterar fonte de dados ou filtros
- `transform.py`: Modificar transformações e limpeza
- `load.py`: Alterar destino ou formato de saída

### Configuração do BigQuery

Certifique-se de que sua tabela BigQuery tenha o schema compatível com os dados da ONS:
```sql
CREATE TABLE `projeto.dataset.tabela` (
  nom_reservatorio STRING,
  tip_reservatorio STRING,
  nom_bacia STRING,
  nom_ree STRING,
  id_subsistema STRING,
  nom_subsistema STRING,
  ear_data DATE,
  -- outros campos numéricos como FLOAT64
);
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Consulte a documentação do Google Cloud
3. Revisite este README para configurações