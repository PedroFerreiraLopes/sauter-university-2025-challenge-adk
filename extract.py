import requests
import json
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data_from_ons_api() -> dict:
    """
    Fetches metadata for a specific data package from the ONS API.

    Returns:
        dict: The JSON response from the ONS API as a Python dictionary.
              Returns an empty dict if the request fails.
    """
    package_id = "61e92787-9847-4731-8b73-e878eb5bc158"
    url = f"https://dados.ons.org.br/api/3/action/package_show?id={package_id}"

    logger.info(f"Fetching data from ONS API for package {package_id}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched data for package {package_id}")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching data from ONS API: {e}")
        return {}


def extract_parquet_for_each_year(parquet_resources: list) -> dict:
    """
    Selects the latest Parquet file for each year from the provided resources.
    Args:
    parquet_resources (list): List of dictionaries representing Parquet resources, 
                              each containing 'name' and 'last_modified'.
    Returns:
    dict: Dictionary mapping each year (str) to its latest resource (dict).
    """
    resources_by_year = defaultdict(list)

    for resource in parquet_resources:
        # Extract year from the resource name
        year = resource['name'].split('-')[-1]
        resources_by_year[year].append(resource)

    latest_resources_per_year = {}

    for year, resources in resources_by_year.items():
        latest_resource = None
        latest_modified_date = None

        for resource in resources:
            modified_date_str = resource.get("last_modified")

            if modified_date_str:
                try:
                    modified_date = datetime.strptime(modified_date_str, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    logging.warning(
                        f"Invalid date format for resource '{resource.get('name')}', skipping."
                    )
                    continue

                if latest_resource is None or modified_date > latest_modified_date:
                    latest_resource = resource
                    latest_modified_date = modified_date

        if latest_resource:
            latest_resources_per_year[year] = latest_resource
            logging.info(f"Selected latest resource for {year}: {latest_resource.get('name')}")

    return latest_resources_per_year


def download_file(url: str, file_path: Path) -> None:
    """
    Downloads a file from a URL and saves it to the specified path.
    Args:
        url (str): URL of the file to download.
        path (Path): Local path where the file will be saved.
    """
    logger.info(f"Starting download: {file_path.name}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded successfully: {file_path.name}")
    except requests.RequestException as e:
        logger.error(f"Failed to download {file_path.name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while downloading {file_path.name}: {e}")


def download_parquet_files_from_ons(last_resources_by_year: dict) -> None:
    """
    Downloads Parquet files from the ONS API based on the provided resources.
    Args:
        last_resources_by_year (Dict): Dictionary mapping year to the latest resource.
    """
    download_dir = Path("./downloads")
    download_dir.mkdir(exist_ok=True)

    for year, resource in last_resources_by_year.items():
        file_url = resource['url']
        file_name = resource['name'] + ".parquet"
        file_path = download_dir / file_name

        download_file(file_url, file_path)

    logger.info("All downloads finished successfully.")


def extract():
    """
    Main function to extract, filter, and download the latest PARQUET files
    from the ONS API for each year.
    """
    logging.info("Starting the extraction process from ONS API.")
   
    ons_json_data: dict = get_data_from_ons_api()

    if not ons_json_data:
        logging.error("No data fetched from ONS API. Exiting process.")
        return

    parquet_resources = [
        resource for resource in ons_json_data['result']['resources'] if resource['format'] == 'PARQUET'
    ]

    if not parquet_resources:
        logging.warning("No PARQUET resources found in ONS data.")
        return

    last_resources_by_year = extract_parquet_for_each_year(
        parquet_resources
    )
    download_parquet_files_from_ons(last_resources_by_year)
    logging.info("Extraction process finished successfully.")


