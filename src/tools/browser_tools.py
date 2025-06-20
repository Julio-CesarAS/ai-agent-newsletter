# src/tools/browser_tools.py
import os
import requests
import json # Importamos a biblioteca JSON
from crewai_tools import BaseTool

class BrowserTool(BaseTool):
    name: str = "news_search_tool"
    description: str = "Busca as notícias mais recentes e relevantes sobre um tópico em inglês."

    def _run(self, query: str) -> str:
        api_key = os.getenv("NEWSAPI_KEY")
        # Buscando 3 artigos por query
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=relevancy&pageSize=3&apiKey={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            
            if not articles:
                return "[]" # Retorna uma lista JSON vazia
            
            # Retorna uma string JSON com os dados estruturados
            return json.dumps([{"title": a["title"], "url": a["url"]} for a in articles])
        except Exception as e:
            print(f"Erro na ferramenta de busca: {e}")
            return "[]" # Retorna uma lista JSON vazia em caso de erro