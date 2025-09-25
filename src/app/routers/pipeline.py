from fastapi import APIRouter, BackgroundTasks, HTTPException
# CORREÇÃO: O import agora é absoluto, começando a partir de 'src.app'
from src.app.pipeline_client import run_pipeline
from src.app.utils.logger import logger

router = APIRouter()

def _execute_pipeline():
    """Função wrapper para ser executada em segundo plano."""
    try:
        job_id = run_pipeline()
        logger.info(f"Pipeline executada com sucesso, job_id={job_id}")
    except Exception as e:
        logger.error(f"Erro ao executar pipeline: {str(e)}")
        # Numa aplicação real, poderíamos notificar um sistema de monitorização aqui
        raise

@router.post("/run", tags=["Pipeline"])
async def trigger_pipeline(background_tasks: BackgroundTasks):
    """
    Dispara a execução completa da pipeline de ETL em segundo plano.
    """
    try:
        logger.info("Recebida requisição para disparar pipeline")
        background_tasks.add_task(_execute_pipeline)
        return {"status": "success", "message": "Pipeline disparada em segundo plano."}
    except Exception as e:
        logger.error(f"Erro ao agendar a pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao tentar disparar a pipeline.")