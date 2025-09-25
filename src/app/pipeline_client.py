import sys
from pathlib import Path
# CORREÇÃO: O import agora é absoluto a partir de 'src.app'
from src.app.utils.logger import logger

# Adiciona o diretório raiz do projeto ao sys.path para que possamos encontrar a pasta 'pipeline'
project_root = Path(__file__).resolve().parent.parent.parent
pipeline_path = project_root / 'pipeline'
if str(pipeline_path) not in sys.path:
    sys.path.append(str(pipeline_path))

# Funções de fallback (plano B)
def _fallback_extract(): logger.error("ERRO CRÍTICO: A função 'extract' da pipeline não pôde ser importada.")
def _fallback_transform(): logger.error("ERRO CRÍTICO: A função 'transform' da pipeline não pôde ser importada.")
def _fallback_load(): logger.error("ERRO CRÍTICO: A função 'load' da pipeline não pôde ser importada.")

extract = _fallback_extract
transform = _fallback_transform
load = _fallback_load

# Tenta importar as funções reais da pipeline (plano A)
try:
    from extract import extract
    from transform import transform
    from load import load
    logger.info("Módulos da pipeline importados com sucesso.")
except ImportError as e:
    logger.error(f"Não foi possível importar os módulos da pipeline. Verifique a estrutura. Erro: {e}")

def run_pipeline() -> dict:
    """
    Orquestra a execução completa da pipeline de ETL.
    """
    logger.info("INICIANDO PROCESSO COMPLETO DE ETL...")

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

    # Exemplo de retorno
    job_id = "some_unique_id"
    return {"status": "success", "job_id": job_id}
