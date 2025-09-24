from google.cloud import bigquery
import os
import logging
from transform import transform


logger = logging.getLogger(__name__)


def load_dataframe_to_bigquery(df, table_id: str, write_mode: str ="WRITE_TRUNCATE"):
    """
    Load a pandas DataFrame into a BigQuery table.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be loaded into BigQuery.
    table_id : str
        Target table in the format "project.dataset.table".
    write_mode : str, optional, default="WRITE_TRUNCATE"
        Write disposition mode:
        - "WRITE_TRUNCATE": Replace the table if it exists.

    Returns
    -------
    google.cloud.bigquery.job.LoadJob
        The completed BigQuery load job.
    """
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
    """
    Main function to transform data and load it into BigQuery.
    """
    logger.info("Starting the load process.")
    df = transform()
    if df is not None:
        load_dataframe_to_bigquery(df, os.getenv("TABLE_ID"))
        logger.info("Load process finished successfully.")
    else:
        logger.warning("No data to load. Skipping BigQuery load.")
    