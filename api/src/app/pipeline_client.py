from utils.logger import logger
import sys
import os

pipeline_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipeline'))
if pipeline_path not in sys.path:
    sys.path.append(pipeline_path)

def extract(): logger.error("ERRO CRÍTICO: A função 'extract' da pipeline não pôde ser importada.")
def transform(): logger.error("ERRO CRÍTICO: A função 'transform' da pipeline não pôde ser importada.")
def load(): logger.error("ERRO CRÍTICO: A função 'load' da pipeline não pôde ser importada.")

try:
    from extract import extract
    from transform import transform
    from load import load
    logger.info("Módulos da pipeline (extract, transform, load) importados com sucesso.")
except ImportError as e:
    logger.error(f"Não foi possível importar os módulos da pipeline. A usar funções de fallback. Erro: {e}")

def run_pipeline():
    
    try:
        logger.info("INICIANDO PROCESSO COMPLETO DE ETL...")

        # 1. Etapa de Extração
        logger.info("--- A executar a etapa de EXTRAÇÃO (extract.py) ---")
        extract()
        logger.info("--- Etapa de EXTRAÇÃO concluída. ---")

        logger.info("--- A executar a etapa de TRANSFORMAÇÃO (transform.py) ---")
        transform()
        logger.info("--- Etapa de TRANSFORMAÇÃO concluída. ---")

        logger.info("--- A executar a etapa de CARREGAMENTO (load.py) ---")
        load()
        logger.info("--- Etapa de CARREGAMENTO concluída. ---")

        logger.info("PROCESSO COMPLETO DE ETL FINALIZADO COM SUCESSO.")
        
        return {"status": "success", "job_id": "some_unique_id"}

    except Exception as e:
        logger.error(f"ERRO CRÍTICO DURANTE A EXECUÇÃO DA PIPELINE: {e}")
    
        return {"status": "error", "message": str(e)}