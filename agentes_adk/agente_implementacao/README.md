# Chatbot Multi-Agente com Google ADK e BigQuery

Este repositório contém o código-fonte de um chatbot avançado construído com o Agent Development Kit (ADK) do Google.  
A aplicação utiliza uma arquitetura multi-agente, onde um orquestrador inteligente delega tarefas para agentes especialistas, capazes de realizar buscas na web e consultas em um banco de dados NoSQL (BigQuery).

O projeto é exposto como uma API web utilizando **FastAPI**, permitindo que seja facilmente integrado a qualquer frontend, como um site, aplicativo móvel ou outro serviço.

---

## 🎯 Propósito da Aplicação

O objetivo deste projeto é demonstrar a criação de um sistema de IA conversacional robusto e modular.  
Em vez de um único modelo monolítico, a aplicação utiliza múltiplos agentes, cada um com uma especialidade distinta:

- **Orquestrador (`orchestrator_agent`)**: Atua como o cérebro do sistema. Ele analisa a pergunta do usuário e, sem respondê-la diretamente, encaminha a tarefa para o agente mais qualificado.  
- **Agente de Busca Web (`sauter_agent`)**: É um especialista na empresa *Sauter Digital*. Ao receber uma pergunta, realiza uma busca focada exclusivamente no site **sauter.digital** para encontrar a informação mais relevante e atualizada.  
- **Agente de Banco de Dados (`bigquery_agent`)**: É um analista de dados que responde a perguntas sobre a ONS. Ele traduz a pergunta do usuário em uma consulta SQL, executa essa consulta em uma tabela no Google BigQuery e formula a resposta com base nos dados retornados.

Essa arquitetura permite que o sistema seja facilmente expandido com novos agentes especialistas no futuro, sem a necessidade de modificar os existentes.

---

## 🛠 Ferramentas e Tecnologias Utilizadas

- **Linguagem:** Python 3.10+  
- **Framework de Agentes:** Google Agent Development Kit (ADK)  
- **Modelo de Linguagem (LLM):** Google Gemini Pro (através da API da Vertex AI)  
- **Framework da API:** FastAPI  
- **Servidor da API:** Uvicorn  
- **Banco de Dados:** Google BigQuery  
- **Autenticação Google Cloud:** Service Accounts  
- **Bibliotecas Principais:**  
  - `google-generativeai`  
  - `google-cloud-bigquery`  
  - `fastapi`  
  - `uvicorn` 

---

## 🚀 Como Rodar a Aplicação

Siga este guia passo a passo para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

- Python 3.10 ou superior  
- Git (para clonar o repositório)  
- Conta no Google Cloud com faturamento ativado (necessário para usar o BigQuery)  
- Docker *(opcional)*, caso queira usar o Redis para gerenciamento de sessão  

---

### 2. Configuração do Ambiente

**Passo 1: Clone o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
cd <NOME_DA_PASTA_DO_PROJETO>
