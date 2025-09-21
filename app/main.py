from fastapi import FastAPI
from app.routers import health, pipeline, data

# Criação da aplicação FastAPI
app = FastAPI(
    title="Reservatórios API",
    version="1.0.0",
    description="API para disparo da pipeline e consulta de dados no BigQuery"
)

# Registra os routers
app.include_router(health.router, prefix="/v1")
app.include_router(pipeline.router, prefix="/v1")
app.include_router(data.router, prefix="/v1")
