from fastapi import APIRouter, HTTPException, Query
from app.services.bigquery_service import fetch_data
from app.utils.logger import logger

router = APIRouter()

@router.get("/data", tags=["Dados"])
async def get_data(
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    offset: int = Query(0, ge=0, description="Número de registros a pular"),
    date: str = Query(None, description="Filtrar por data no formato YYYY-MM-DD")
):
    try:
        logger.info(f"Consulta ao BigQuery (limit={limit}, offset={offset}, date={date})")
        rows = fetch_data(limit=limit, offset=offset, date=date)
        return {"count": len(rows), "rows": rows}
    except Exception as e:
        logger.error(f"Erro ao consultar BigQuery: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar dados: {str(e)}")
