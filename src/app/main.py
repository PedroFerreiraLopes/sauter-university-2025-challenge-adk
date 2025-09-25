from fastapi import FastAPI
# CORREÇÃO: O import agora começa a partir de 'src.app'
from src.app.routers import health, pipeline, data

# Criação da aplicação FastAPI
app = FastAPI(
    title="Reservatórios API",
    version="1.0.0",
    description="API para disparo da pipeline e consulta de dados no BigQuery"
)

# Registrando routers
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(pipeline.router, prefix="/api/v1/pipeline", tags=["Pipeline"])
app.include_router(data.router, prefix="/api/v1/data", tags=["Data"])
