from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools import google_search
from ferramentas.sauter_busca_tool import perform_google_site_search



sauter_agent = Agent(
    name="sauter_agent",
    model="gemini-2.0-flash",
    description="Responde com as informações da Sauter quando o usuário perguntar.",
    instruction="""
        Você é um assistente especialista na empresa Sauter.
        Sua ÚNICA função é responder perguntas sobre a Sauter usando as informações do site oficial deles.
        Para fazer isso, você DEVE usar a ferramenta 'perform_google_site_search'.
        
        Processo:
        1. Analise a pergunta do usuário (ex: "quais os serviços da sauter?").
        2. Extraia as palavras-chave principais (ex: "serviços").
        3. Chame a ferramenta 'perform_sauter_site_search' com essas palavras-chave como o parâmetro 'query'.
        4. Com base nos resultados retornados pela ferramenta, formule uma resposta completa e útil para o usuário.
        5. Se a ferramenta não retornar nenhuma informação, informe ao usuário que não foi possível encontrar a resposta no site oficial""",
    tools=[FunctionTool(func=perform_google_site_search)]
)