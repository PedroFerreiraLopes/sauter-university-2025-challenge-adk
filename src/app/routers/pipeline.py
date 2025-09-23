from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.pipeline_client import run_pipeline 
from app.utils.logger import logger

router = APIRouter()

def _execute_pipeline():
    try:
        job_id = run_pipeline()
        logger.info(f"Pipeline executada com sucesso, job_id={job_id}")
    except Exception as e:
        logger.error(f"Erro ao executar pipeline: {str(e)}")
        raise

@router.post("/pipeline", tags=["Pipeline"])
async def trigger_pipeline(background_tasks: BackgroundTasks):
   
    try:
        logger.info("Recebida requisição para disparar pipeline")
        background_tasks.add_task(_execute_pipeline)
        return {"status": "Pipeline em execução"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao disparar pipeline: {str(e)}")
