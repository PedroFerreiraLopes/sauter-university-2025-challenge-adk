from google.cloud import bigquery
from google.adk.tools import FunctionTool
from decimal import Decimal


def normalize_value(value):
    """Normaliza qualquer valor para ser JSON serializable."""
    if isinstance(value, Decimal):
        # se o valor é inteiro, mantém como int
        if value == value.to_integral_value():
            return int(value)
        # senão, deixa como string para não perder precisão em valores decimais
        return str(value)
    return value

def run_bigquery_sql(query: str) -> list:
    """Executa uma consulta SQL no Google BigQuery e retorna o resultado em formato de lista de dicionários."""
    try:
        print(f"--- Executando a seguinte query no BigQuery ---\n{query}\n-------------------------------------------------")
        
        client = bigquery.Client()
        query_job = client.query(query)
        
        results = []
        for row in query_job.result():
            row_dict = {k: normalize_value(v) for k, v in dict(row).items()}
            results.append(row_dict)
        
        print(f"--- Resultado da Query ---\n{results}\n----------------------------")
        
        return results
    except Exception as e:
        error_message = f"Erro ao executar a query no BigQuery: {e}"
        print(error_message)
        return [{"erro": error_message}]

run_bigquery_sql_tool = FunctionTool(run_bigquery_sql)