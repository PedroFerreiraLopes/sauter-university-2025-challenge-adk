from pipeline_client import run_pipeline
from utils.logger import logger

if __name__ == "__main__":
    logger.info("--- INICIANDO TESTE DE INTEGRAÇÃO DA PIPELINE ---")

    # Chamamos a função principal do nosso orquestrador
    run_pipeline()

    logger.info("--- TESTE DE INTEGRAÇÃO DA PIPELINE CONCLUÍDO ---")