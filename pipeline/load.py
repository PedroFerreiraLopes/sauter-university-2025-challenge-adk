from google.cloud import bigquery
import os
import logging
from transform import transform


logger = logging.getLogger(__name__)


def load_dataframe_to_bigquery(df, table_id: str, write_mode: str ="WRITE_TRUNCATE"):
    
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )
    
    job.result()
    logger.info("Data loaded successfully into table %s.", table_id)
    return job

def load():
    
    logger.info("Starting the load process.")
    df = transform()
    if df is not None:
        load_dataframe_to_bigquery(df, os.getenv("TABLE_ID"))
        logger.info("Load process finished successfully.")
    else:
        logger.warning("No data to load. Skipping BigQuery load.")
    