import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def transform():
    
    logger.info("A iniciar o processo de TRANSFORMAÇÃO de dados.")

    logger.info("Processo de TRANSFORMAÇÃO finalizado com sucesso.")

if __name__ == "__main__":
    transform()
