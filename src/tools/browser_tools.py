# src/tools/browser_tools.py
import os
import requests
import json
from typing import Type
from pydantic import BaseModel, Field

class NewsSearchInput(BaseModel):
    """Input schema for NewsSearchTool."""
    query: str = Field(..., description="Search query for news articles")

class NewsSearchTool:
    name: str = "news_search_tool"
    description: str = "Busca as notícias mais recentes e relevantes sobre um tópico em inglês."
    args_schema: Type[BaseModel] = NewsSearchInput

    def _run(self, query: str) -> str:
        """Execute the tool."""
        api_key = os.getenv("NEWSAPI_KEY")
        # Buscando 3 artigos por query (ordenado por data para ter artigos mais recentes)
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&from={yesterday}&pageSize=3&apiKey={api_key}"
        
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

# Instância da ferramenta
news_search_tool = NewsSearchTool()