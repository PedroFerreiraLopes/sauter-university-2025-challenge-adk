import requests
import json
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configuração básica do logging para exibir mensagens de informação
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_data_from_ons_api() -> dict:
    
    package_id = "61e92787-9847-4731-8b73-e878eb5bc158"
    url = f"https://dados.ons.org.br/api/3/action/package_show?id={package_id}"

    logger.info(f"Buscando dados da API do ONS para o pacote {package_id}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro para respostas HTTP ruins (4xx ou 5xx)
        data = response.json()
        logger.info(f"Dados do pacote {package_id} obtidos com sucesso.")
        return data
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados da API do ONS: {e}")
        return {}


def extract_parquet_for_each_year(parquet_resources: list) -> dict:
    
    resources_by_year = defaultdict(list)

    for resource in parquet_resources:
        # Extrai o ano do nome do recurso (ex: 'geracao-usina-ho-2023')
        try:
            year = resource['name'].split('-')[-1]
            if year.isdigit():
                resources_by_year[year].append(resource)
        except (IndexError, KeyError):
            logger.warning(f"Não foi possível extrair o ano do recurso: {resource.get('name', 'N/A')}")

    latest_resources_per_year = {}

    for year, resources in resources_by_year.items():
        latest_resource = None
        latest_modified_date = None

        for resource in resources:
            modified_date_str = resource.get("last_modified")

            if modified_date_str:
                try:
                    # Tenta converter a data de modificação para um objeto datetime
                    modified_date = datetime.strptime(modified_date_str, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    logging.warning(
                        f"Formato de data inválido para o recurso '{resource.get('name')}', pulando."
                    )
                    continue

                if latest_resource is None or modified_date > latest_modified_date:
                    latest_resource = resource
                    latest_modified_date = modified_date

        if latest_resource:
            latest_resources_per_year[year] = latest_resource
            logger.info(f"Recurso mais recente para {year} selecionado: {latest_resource.get('name')}")

    return latest_resources_per_year


def download_file(url: str, file_path: Path) -> None:
    
    logger.info(f"Iniciando download: {file_path.name}")
    try:
        response = requests.get(url, stream=True) # Usar stream para arquivos grandes
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Download concluído: {file_path.name}")
    except requests.RequestException as e:
        logger.error(f"Falha no download de {file_path.name}: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado durante o download de {file_path.name}: {e}")


def download_parquet_files_from_ons(last_resources_by_year: dict) -> None:
    
    download_dir = Path("./downloads")
    download_dir.mkdir(exist_ok=True)

    for year, resource in last_resources_by_year.items():
        file_url = resource['url']
        # O nome do arquivo já é descritivo, podemos mantê-lo
        file_name = f"{resource['name']}.parquet"
        file_path = download_dir / file_name

        download_file(file_url, file_path)

    logger.info("Todos os downloads foram concluídos.")


def extract():
    
    logging.info("Iniciando o processo de extração da API do ONS.")
    
    ons_json_data: dict = get_data_from_ons_api()

    if not ons_json_data:
        logging.error("Nenhum dado obtido da API do ONS. Processo encerrado.")
        return

    # Filtra apenas os recursos que estão no formato PARQUET
    parquet_resources = [
        resource for resource in ons_json_data['result']['resources'] if resource['format'].upper() == 'PARQUET'
    ]

    if not parquet_resources:
        logging.warning("Nenhum recurso no formato PARQUET foi encontrado nos dados do ONS.")
        return

    last_resources_by_year = extract_parquet_for_each_year(
        parquet_resources
    )
    
    if not last_resources_by_year:
        logging.warning("Nenhum recurso válido por ano foi selecionado para download.")
        return

    download_parquet_files_from_ons(last_resources_by_year)
    logging.info("Processo de extração finalizado com sucesso.")

# Ponto de entrada para executar o script diretamente
if __name__ == "__main__":
    extract()