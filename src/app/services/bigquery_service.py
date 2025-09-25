from google.cloud import bigquery
# CORREÇÃO: O import agora é absoluto, começando a partir de 'src.app'
from src.app.utils.logger import logger

def fetch_data(limit: int, offset: int, date: str | None) -> list:
    """
    Busca dados da tabela do BigQuery.
    """
    try:
        client = bigquery.Client()
        # Substitua pelo seu projeto e tabela corretos
        table_id = "seu-projeto.seu_dataset.sua_tabela"
        
        query = f"""
            SELECT *
            FROM `{table_id}`
        """
        
        if date:
            query += f" WHERE DATE(sua_coluna_de_data) = '{date}'"
            
        query += f" LIMIT {limit} OFFSET {offset}"

        logger.info(f"Executando query no BigQuery: {query}")
        query_job = client.query(query)
        results = [dict(row) for row in query_job]
        
        logger.info(f"Encontrados {len(results)} registros.")
        return results
    except Exception as e:
        logger.error(f"Erro na comunicação com o BigQuery: {e}")
        # Lançar a exceção para ser tratada pelo router
        raise
