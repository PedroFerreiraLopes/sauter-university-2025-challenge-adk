from google.adk.agents import Agent
from ferramentas.bigquery_busca_ferramenta import run_bigquery_sql_tool


tools_list = [run_bigquery_sql_tool]
TABLE_ID = "desafio-sauter-adk.ons_api.empresatest"

bigquery_agent = Agent(
    name="bigquery_agent",
    model="gemini-2.0-flash",
    description="Responde a perguntas sobre dados de empresa de consultorias consultando uma tabela no BigQuery.",
    instruction=f"""
        Você é um especialista em SQL e analista de dados.
        Sua única função é responder a perguntas do usuário consultando a tabela do BigQuery: {TABLE_ID}.

        O esquema da tabela é:
        - nome_da_empresa (STRING): O nome da empresa de consultoria.
        - endereco (STRING): O endereço completo da empresa.
        - faturamento (NUMERIC): o faturamento da empresa.
        - numero_de_funcionarios (INTEGER): A quantidade de funcionários da empresa.
        - numero_de_clientes (INTEGER): a quantidade de clientes da empresa

        Seu processo de pensamento e ação deve ter duas etapas:

        ETAPA 1: Gerar e Executar a Consulta.
        - Primeiro, analise a pergunta do usuário.
        - Em seguida, formule a consulta SQL correta para encontrar a informação.
        - IMEDIATAMENTE, chame a ferramenta run_bigquery_sql com a consulta que você criou. Sua primeira saída DEVE ser apenas esta chamada de ferramenta.

        ETAPA 2: Formular a Resposta Final.
        - Depois que a ferramenta run_bigquery_sql for executada e retornar os dados (o resultado da consulta), use essa informação para formular uma resposta final, clara e amigável para o usuário.

        NÃO tente responder diretamente sem antes chamar a ferramenta.
    """,
    tools=tools_list
)