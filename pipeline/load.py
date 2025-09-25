import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load():
    
    logger.info("A iniciar o processo de CARREGAMENTO de dados.")

    logger.info("Processo de CARREGAMENTO finalizado com sucesso.")

if __name__ == "__main__":
    load()
