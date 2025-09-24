import os
import logging
import asyncio


PATH_PARA_O_ARQUIVO_JSON = ""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH_PARA_O_ARQUIVO_JSON
from orchestrator.main_orchestrator import orchestrator_agent



os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "desafio-sauter-adk"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

from google.oauth2 import service_account
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import vertexai

for logger_name in ["google.auth", "urllib3", "httpcore", "httpx"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


async def call_agent(query: str, runner: Runner, user_id: str, session_id: str):
    print(f">>> Pergunta: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content:
            print(f"<<< Resposta: {event.content.parts[0].text}")


async def main():
    """
    Função principal que configura e executa o agente.
    Toda a lógica async está contida aqui.
    """
    
    """  vertexai.init(
        project="desafio-sauter-adk",
        location="us-central1",
    ) """
        
    APP_NAME = "multi_agent_app"
    USER_ID = "user_1"
    SESSION_ID = "session_orquestrador"

    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Sessão '{SESSION_ID}' criada e registrada com sucesso.")

    print("\nDigite 'sair' para encerrar a conversa.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break
        await call_agent(user_input, runner, USER_ID, SESSION_ID)


if _name_ == "_main_":
    asyncio.run(main())