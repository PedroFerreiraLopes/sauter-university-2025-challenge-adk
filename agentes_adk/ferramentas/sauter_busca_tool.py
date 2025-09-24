from googleapiclient.discovery import build

def perform_google_site_search(query: str) -> str:
    """
    Realiza uma busca focada no site sauter.digital usando a API de Busca Customizada do Google.
    Use esta ferramenta para responder perguntas sobre a Sauter.
    """
    try:
    
        API_KEY = "AIzaSyD-yHmpGRFlQerYnv2AzvvdK0trPOzwwdM"
        SEARCH_ENGINE_ID = "f06b02730eaf24e5a"

        print(f"--- 🔎 Realizando busca no Google por: '{query}' em sauter.digital ---")
        
        # Cria o serviço de busca
        service = build("customsearch", "v1", developerKey=API_KEY)
        
        # Executa a busca
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=5).execute()
        
        if 'items' not in res or not res['items']:
            return "Nenhum resultado encontrado no site sauter.digital para a busca realizada via Google."

        # Formata os resultados
        results = res['items']
        formatted_results = "\n\n".join(
            [f"Título: {item['title']}\nFonte: {item['link']}\nConteúdo: {item.get('snippet', '')}" for item in results]
        )
        print(f"--- ✅ Resultados encontrados via Google ---")
        return formatted_results

    except Exception as e:
        print(f"--- ❌ Erro na busca com Google API: {e} ---")
        return f"Ocorreu um erro ao tentar buscar com a Google API: {e}"