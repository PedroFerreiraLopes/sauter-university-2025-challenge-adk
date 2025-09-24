from google.adk.agents import Agent
from agents.agente_sauter import sauter_agent
from agents.agente_bigquery import bigquery_agent


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
    sub_agents=[sauter_agent, bigquery_agent]
)