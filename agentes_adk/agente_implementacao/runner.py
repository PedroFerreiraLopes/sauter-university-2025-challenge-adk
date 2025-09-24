import os
import logging
import asyncio
from typing import Optional
from uuid import uuid4
from dotenv import load_dotenv

# --- Importações da API ---
from fastapi import FastAPI
from pydantic import BaseModel

# --- Importações do ADK ---
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from orquestrador.orquestrador import orchestrator_agent

# ==============================================================================
# ETAPA 1: CONFIGURAÇÃO INICIAL (Executada apenas uma vez ao iniciar a API)
# ==============================================================================

# --- Configuração de Ambiente ---
load_dotenv()
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")


# --- Configuração de Logging ---
for logger_name in ["google.auth", "urllib3", "httpcore", "httpx"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)

# --- Inicialização do Runner do ADK (Singleton) ---
APP_NAME = "multi_agent_api"
session_service = InMemorySessionService()
runner = Runner(
    agent=orchestrator_agent,
    app_name=APP_NAME,
    session_service=session_service
)
print("✅ ADK Runner inicializado com sucesso.")

# --- Inicialização do FastAPI ---
app = FastAPI(
    title="Chatbot Multi-Agente API",
    description="Uma API para interagir com o orquestrador de agentes do ADK.",
    version="1.0.0"
)

# ==============================================================================
# ETAPA 2: DEFINIÇÃO DOS MODELOS DE DADOS DA API
# ==============================================================================

class ChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    user_id: str
    session_id: str

# ==============================================================================
# ETAPA 3: DEFINIÇÃO DO ENDPOINT DA API
# ==============================================================================

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Envia uma mensagem para o chatbot e recebe a resposta final.
    """
    # --- Gerenciamento de Sessão ---
    user_id = request.user_id or f"user_{uuid4()}"
    session_id = request.session_id or f"session_{uuid4()}"

    # <<< A CORREÇÃO ESTÁ AQUI: Simplesmente criamos a sessão a cada chamada,
    # espelhando a lógica do seu runner.py original.
    # Isso garante que a sessão SEMPRE exista antes do runner ser chamado.
    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        logging.info(f"Sessão criada com sucesso: {session_id}")
    except Exception:
        # Este 'except' lida com o caso onde a sessão já existe de uma
        # requisição anterior com o mesmo session_id. Apenas logamos e continuamos.
        logging.info(f"Sessão já existente: {session_id}. Continuando.")
        pass

    # --- Lógica de Chamada do Agente ---
    content = types.Content(role='user', parts=[types.Part(text=request.query)])
    final_response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content:
            final_response = event.content.parts[0].text
            break

    if not final_response:
        final_response = "Desculpe, não consegui gerar uma resposta."

    logging.info(f"Resposta final: {final_response}")

    return ChatResponse(
        response=final_response,
        user_id=user_id,
        session_id=session_id
    )

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "API do Chatbot Multi-Agente está no ar. Acesse /docs para a documentação."}