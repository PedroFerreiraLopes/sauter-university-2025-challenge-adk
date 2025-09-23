from app.utils.logger import logger

async def run_pipeline() -> dict:
    
    logger.info("Pipeline disparada (mock).")
    return {"status": "success", "message": "Pipeline disparada com sucesso"}
