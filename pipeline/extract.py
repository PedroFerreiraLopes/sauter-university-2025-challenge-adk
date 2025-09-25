import requests
import json
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_data_from_ons_api() -> dict:
    
    package_id = "61e92787-9847-4731-8b73-e878eb5bc158"
    url = f"https://dados.ons.org.br/api/3/action/package_show?id={package_id}"
    logger.info(f"A buscar dados da API do ONS para o pacote {package_id}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Dados do pacote {package_id} obtidos com sucesso.")
        return data
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados da API do ONS: {e}")
        return {}


def extract_parquet_for_each_year(parquet_resources: list) -> dict:
    
    resources_by_year = defaultdict(list)

    for resource in parquet_resources:
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
                    logging.warning(f"Formato de data inválido para o recurso '{resource.get('name')}', a ignorar.")
                    continue

                if latest_resource is None or modified_date > latest_modified_date:
                    latest_resource = resource
                    latest_modified_date = modified_date

        if latest_resource:
            latest_resources_per_year[year] = latest_resource
            logging.info(f"Recurso mais recente para {year} selecionado: {latest_resource.get('name')}")
    return latest_resources_per_year


def download_file(url: str, file_path: Path) -> None:
    
    logger.info(f"A iniciar o download: {file_path.name}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Download concluído com sucesso: {file_path.name}")
    except requests.RequestException as e:
        logger.error(f"Falha no download de {file_path.name}: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado durante o download de {file_path.name}: {e}")


def download_parquet_files_from_ons(last_resources_by_year: dict) -> None:
    
    download_dir = Path("./downloads")
    download_dir.mkdir(exist_ok=True)

    for year, resource in last_resources_by_year.items():
        file_url = resource['url']
        file_name = resource['name'] + ".parquet"
        file_path = download_dir / file_name

        download_file(file_url, file_path)

    logger.info("Todos os downloads foram concluídos.")



def extract():
    
    logger.info("A iniciar o processo de extração da API do ONS.")
    
    ons_json_data: dict = get_data_from_ons_api()

    if not ons_json_data:
        logger.error("Nenhum dado obtido da API do ONS. A sair do processo.")
        return


    parquet_resources = [
        resource for resource in ons_json_data['result']['resources'] if resource['format'] == 'PARQUET'
    ]

    if not parquet_resources:
        logging.warning("Nenhum recurso PARQUET encontrado nos dados do ONS.")
        return

    last_resources_by_year = extract_parquet_for_each_year(parquet_resources)
    download_parquet_files_from_ons(last_resources_by_year)
    logger.info("Processo de extração finalizado com sucesso.")





if __name__ == "__main__":
    extract()