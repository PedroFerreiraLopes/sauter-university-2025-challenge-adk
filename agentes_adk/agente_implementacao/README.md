Chatbot Multi-Agente com Google ADK e BigQuery
Este repositório contém o código-fonte de um chatbot avançado construído com o Agent Development Kit (ADK) do Google. A aplicação utiliza uma arquitetura multi-agente, onde um orquestrador inteligente delega tarefas para agentes especialistas, capazes de realizar buscas na web e consultas em um banco de dados NoSQL (BigQuery).

O projeto é exposto como uma API web utilizando FastAPI, permitindo que seja facilmente integrado a qualquer frontend, como um site, aplicativo móvel ou outro serviço.

🎯 Propósito da Aplicação
O objetivo deste projeto é demonstrar a criação de um sistema de IA conversacional robusto e modular. Em vez de um único modelo monolítico, a aplicação utiliza múltiplos agentes, cada um com uma especialidade distinta:

Orquestrador (orchestrator_agent): Atua como o cérebro do sistema. Ele analisa a pergunta do usuário e, sem respondê-la diretamente, encaminha a tarefa para o agente mais qualificado.

Agente de Busca Web (sauter_agent): É um especialista na empresa "Sauter Digital". Ao receber uma pergunta, ele realiza uma busca focada exclusivamente no site sauter.digital para encontrar a informação mais relevante e atualizada.

Agente de Banco de Dados (bigquery_agent): É um analista de dados que responde a perguntas sobre um conjunto de empresas de consultoria. Ele traduz a pergunta do usuário em uma consulta SQL, executa essa consulta em uma tabela no Google BigQuery e formula a resposta com base nos dados retornados.

Essa arquitetura permite que o sistema seja facilmente expandido com novos agentes especialistas no futuro, sem a necessidade de modificar os existentes.

🛠 Ferramentas e Tecnologias Utilizadas
Linguagem: Python 3.10+

Framework de Agentes: Google Agent Development Kit (ADK)

Modelo de Linguagem (LLM): Google Gemini Pro (através da API da Vertex AI)

Framework da API: FastAPI

Servidor da API: Uvicorn

Banco de Dados: Google BigQuery

Autenticação Google Cloud: Service Accounts

Bibliotecas Principais: google-generativeai, google-cloud-bigquery, fastapi, uvicorn, redis (para o serviço de sessão opcional).

🚀 Como Rodar a Aplicação
Siga este guia passo a passo para configurar e executar o projeto em sua máquina local.

1. Pré-requisitos
Python 3.10 ou superior: Instale o Python.

Git: Para clonar o repositório.

Conta no Google Cloud: Com um projeto criado e o faturamento ativado (necessário para usar a Vertex AI e o BigQuery).

Docker (Opcional): Se você decidir usar o Redis para gerenciamento de sessão, ter o Docker é a maneira mais fácil de rodá-lo localmente.

2. Configuração do Ambiente
Passo 1: Clone o Repositório
Abra seu terminal e clone este repositório para a sua máquina.

git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
cd <NOME_DA_PASTA_DO_PROJETO>

Passo 2: Crie e Ative um Ambiente Virtual
É uma boa prática isolar as dependências do projeto.

# Criar o ambiente virtual
python -m venv env

# Ativar no Windows
.\env\Scripts\activate

# Ativar no macOS/Linux
source env/bin/activate

Passo 3: Instale as Dependências
Todas as bibliotecas necessárias estão listadas no arquivo requirements.txt.

pip install -r requirements.txt

Passo 4: Configure a Autenticação com o Google Cloud (Passo Crucial)
O ADK precisa se autenticar para usar os serviços do Google Cloud.

No seu Console do Google Cloud, navegue até "IAM e Admin" > "Contas de Serviço".

Crie uma nova conta de serviço. Dê a ela os papéis de "Usuário da Vertex AI" e "Usuário do BigQuery".

Após criar a conta, vá na aba "Chaves", clique em "Adicionar Chave" > "Criar nova chave" e escolha o formato JSON. Um arquivo .json será baixado.

Renomeie este arquivo para credentials.json e coloque-o na raiz do seu projeto.

Abra o arquivo api.py e verifique se o caminho para o arquivo de credenciais está correto na linha abaixo. Se você colocou o arquivo na raiz, o caminho pode ser simplesmente "credentials.json".

# Dentro do arquivo api.py
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

3. Executando a API
Com tudo configurado, inicie o servidor FastAPI com o Uvicorn. O comando --reload faz com que o servidor reinicie automaticamente sempre que você salvar uma alteração no código.

uvicorn api:app --reload

Se tudo deu certo, você verá uma saída parecida com esta no seu terminal:

INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
✅ ADK Runner inicializado com sucesso.
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Sua API agora está no ar!

4. Como Usar a API
A maneira mais fácil de interagir com a API é através da documentação interativa gerada automaticamente pelo FastAPI.

Passo 1: Acesse a Documentação
Abra seu navegador e vá para: http://127.0.0.1:8000/docs

Passo 2: Faça sua Primeira Pergunta

Na página da documentação, você verá o endpoint POST /chat. Clique para expandi-lo.

Clique no botão "Try it out".

No campo "Request body", digite sua pergunta.

Exemplo de pergunta para o Agente BigQuery:

{
  "query": "qual o endereço da empresa de consultorias Moda Fashion?"
}

Exemplo de pergunta para o Agente Sauter:

{
  "query": "quais os serviços da sauter?"
}

Clique no botão "Execute". A resposta da API aparecerá logo abaixo.

Passo 3: Continue uma Conversa
Para manter o contexto, você precisa enviar de volta o session_id que recebeu na resposta anterior.

Copie o session_id da resposta da sua primeira pergunta.

Faça uma nova requisição, mas desta vez, inclua o session_id no corpo da requisição.

Exemplo de pergunta de continuação:

{
  "query": "e qual o faturamento dela?",
  "session_id": "session_a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
}