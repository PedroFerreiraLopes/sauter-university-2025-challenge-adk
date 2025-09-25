from google.cloud import bigquery
from tenacity import retry, wait_fixed, stop_after_attempt
from utils.logger import logger

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def fetch_data(limit: int = 100, offset: int = 0, date: str = None):
    
    client = bigquery.Client()

    query = "SELECT * FROM `meu-projeto.energia.ear_reservatorio`"
    if date:
        query += f" WHERE data = '{date}'"
    query += f" LIMIT {limit} OFFSET {offset}"

    logger.info(f"Executando query no BigQuery: {query}")
    query_job = client.query(query)
    results = query_job.result()

    return [dict(row) for row in results]
