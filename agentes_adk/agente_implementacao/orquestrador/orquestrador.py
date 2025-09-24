from google.adk.agents import Agent
from agents.translate_agent import translate_agent
from agents.math_agent import math_agent
from agents.time_agent import time_agent
from agents.search_sauter_agent import sauter_agent
from agents.bigquery_agent import bigquery_agent


orchestrator_agent = Agent(
    name="orchestrator",
    model= "gemini-2.0-flash",
    description="Orquestrador que entende a tarefa e delega para o agente apropriado.",
    instruction="""
       Você é um roteador de tarefas inteligente. Sua única função é analisar a pergunta do usuário e delegar para o agente especialista correto.
        - Para perguntas sobre a empresa Sauter, delegue para 'sauter_agent'.
        - Para perguntas que envolvam dados sobre empresas de consultorias delegue para 'bigquery_agent'.

        NUNCA tente responder a uma pergunta diretamente. Sua única ação deve ser chamar a ferramenta transfer_to_agent.
    """,
    sub_agents=[translate_agent, bigquery_agent]
)