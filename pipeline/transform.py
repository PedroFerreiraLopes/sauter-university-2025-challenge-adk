import pandas as pd 
import os 
import logging 
from typing import List, Optional 

logger = logging.getLogger(__name__)


def list_parquet_files(directory: str) -> List[str]: 
    """
    List all parquet files in a given directory.
    Args:
        directory (str): Path to the directory containing parquet files.
    Returns:
        List[str]: List of full paths to parquet files.
    """
    files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".parquet")
    ]
    logger.info("Found %d parquet file(s) in directory: %s", len(files), directory)
    return files


def load_parquet_files(file_paths: List[str]) -> List[pd.DataFrame]:
    """
    Load parquet files into a list of pandas DataFrames.
    Args:
        file_paths (List[str]): List of parquet file paths.
    Returns:
        List[pd.DataFrame]: List of DataFrames loaded from the parquet files.
    """    
    dataframes = []
    for path in file_paths:
        try:
            df = pd.read_parquet(path)
            dataframes.append(df)
            logger.info("Successfully loaded file: %s", path)
        except Exception as error:
            logger.error("Error reading '%s': %s", path, error)
    return dataframes


def combine_dataframes(dataframes: List[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Combine a list of pandas DataFrames into a single DataFrame.    
    Args:
        dataframes (List[pd.DataFrame]): List of pandas DataFrames.
    Returns:
        Optional[pd.DataFrame]: A single combined DataFrame, or None if the list is empty.
    """
    if not dataframes:
        logger.warning("No DataFrames to combine.")
        return None
    logger.info("Combining %d DataFrames into one.", len(dataframes))
    
    return pd.concat(dataframes, ignore_index=True)


def drop_unused_columns(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    """
    Removes unnecessary columns from a DataFrame.

    Parameters:
    df (pd.DataFrame): The original DataFrame.
    columns_to_drop (list): List of column names to remove.

    Returns:
    pd.DataFrame: A new DataFrame without the unwanted columns.
    """
    columns_existing = [col for col in columns_to_drop if col in df.columns]

    cleaned_df = df.drop(columns=columns_existing)
    
    return cleaned_df


def normalize_dataframe(combined_df):
    """
        Normalize the data types of a DataFrame.
     Parameters
    ----------
    combined_df : pandas.DataFrame
        Input DataFrame containing mixed data types.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with standardized column types.
    """
    string_cols = ['nom_reservatorio', 'tip_reservatorio', 'nom_bacia', 
                   'nom_ree', 'id_subsistema', 'nom_subsistema']
    
    for col in combined_df.columns:
        if col in string_cols:
            combined_df[col] = combined_df[col].astype(str)
        elif col == 'ear_data':
            combined_df[col] = pd.to_datetime(combined_df[col], errors='coerce')
        else:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').astype(float)

    return combined_df        


def transform():
    """
    Combines downloaded Parquet files into a single DataFrame and drops unused columns.
    
    Returns:
        pandas.DataFrame or None: Combined DataFrame, or None if no files were loaded.
    """
    download_dir = "./downloads"

    parquet_files = list_parquet_files(download_dir)

    if not parquet_files:
        logger.warning("No parquet files found in the download directory.")
        return

    dataframes = load_parquet_files(parquet_files)

    if not dataframes:
        logger.warning("No DataFrames were successfully loaded.")
        return

    combined_df = combine_dataframes(dataframes)

    if combined_df is not None:
        logger.info("Final DataFrame shape: %s", combined_df.shape)


    columns_to_drop = [
    'cod_resplanejamento',
    'id_subsistema_jusante', 
    'nom_subsistema_jusante',
    'earmax_reservatorio_subsistema_jusante_mwmes',
    ]

    combined_df = drop_unused_columns(combined_df, columns_to_drop)    

    return combined_df