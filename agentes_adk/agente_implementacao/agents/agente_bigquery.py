from google.adk.agents import Agent
from ferramentas.bigquery_busca_ferramenta import run_bigquery_sql_tool


tools_list = [run_bigquery_sql_tool]
TABLE_ID = "desafio-sauter-adk.teste.Classificação_do_Estado_do_Reservatório"

bigquery_agent = Agent(
    name="bigquery_agent",
    model="gemini-2.0-flash",
    description="Responde a perguntas sobre dados sobre a ONS (Operador Nacional do Sistema Elétrico) consultando uma tabela no BigQuery.",
    instruction=f"""
        Você é um especialista em SQL e analista de dados.
        Sua única função é responder a perguntas do usuário consultando a tabela do BigQuery: {TABLE_ID}.

        O esquema da tabela é:
        - nom_reservatorio (STRING): O nome da empresa de consultoria (aqui os nomes estão em upper case).
        - ear_data (DATE): Data do reservório naquele dia.
        - ear_reservatorio_percentual (FLOAT): O percentual do reservatório.
        - classificacao (STRING): A classificação do reservatorio.


        Seu processo de pensamento e ação deve ter duas etapas:

        ETAPA 1: Gerar e Executar a Consulta.
        - Primeiro, analise a pergunta do usuário.
        - Em seguida, formule a consulta SQL correta para encontrar a informação.
        - IMEDIATAMENTE, chame a ferramenta run_bigquery_sql com a consulta que você criou. Sua primeira saída DEVE ser apenas esta chamada de ferramenta.
        PS: A coluna 'nom_reservatorio' está com os dados todos em caixa alta. Na clásula where, formatar para buscar o nome em caixa alta 
        (ex: WHERE nom_reservatorio = 'ONS' ao invés de 'Ons' ou 'ons').

        ETAPA 2: Formular a Resposta Final.
        - Depois que a ferramenta run_bigquery_sql for executada e retornar os dados (o resultado da consulta), use essa informação para formular uma resposta final, clara e amigável para o usuário.

        NÃO tente responder diretamente sem antes chamar a ferramenta.
    """,
    tools=tools_list
)