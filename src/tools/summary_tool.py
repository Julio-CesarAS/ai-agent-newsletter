# src/tools/summary_tool.py
import os
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
import requests
from typing import Type
from pydantic import BaseModel, Field

class SummaryInput(BaseModel):
    """Input schema for SummaryTool."""
    url: str = Field(..., description="URL of the website to summarize")

class SummaryTool:
    name: str = "summary_tool"
    description: str = "Recebe uma URL de website, extrai seu conteúdo e gera um resumo conciso."
    args_schema: Type[BaseModel] = SummaryInput

    def _run(self, url: str) -> str:
        """Execute the tool."""
        print(f"\n--- [SummaryTool] Iniciando para a URL: {url} ---")
        llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
        
        print("Etapa 1: Raspando o conteúdo do site...")
        
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            # Primeiro tentativa com headers personalizados
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover scripts e estilos
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Tentar extrair conteúdo de diferentes tags
            content_selectors = [
                'article',
                '.article-content',
                '.content',
                '.post-content',
                '.story-body',
                'main',
                '[role="main"]'
            ]
            
            full_text = ""
            
            # Tentar seletores específicos primeiro
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    text_elements = elements[0].find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if text_elements:
                        full_text = ' '.join([elem.get_text().strip() for elem in text_elements if elem.get_text().strip()])
                        break
            
            # Se não encontrou conteúdo específico, usar método geral
            if not full_text.strip():
                text_elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
                full_text = ' '.join([elem.get_text().strip() for elem in text_elements if elem.get_text().strip()])
            
            if not full_text.strip():
                return "Não foi possível extrair conteúdo textual significativo da URL."
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("⚠️  Rate limit atingido, aguardando...")
                import time
                time.sleep(2)
                try:
                    # Segunda tentativa após delay
                    response = requests.get(url, headers=headers, timeout=15)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text_elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
                    full_text = ' '.join([elem.get_text().strip() for elem in text_elements if elem.get_text().strip()])
                    if not full_text.strip():
                        return "Não foi possível extrair conteúdo textual significativo da URL após segunda tentativa."
                except:
                    return f"Site temporariamente indisponível (Rate limit). Erro: {e}"
            elif e.response.status_code in [403, 420]:
                return f"Site bloqueou o acesso automatizado. Erro: {e}"
            else:
                return f"Erro HTTP ao acessar a URL: {e}"
        except Exception as e:
            return f"Erro ao acessar ou processar a URL: {e}"

        print("Etapa 2: Fatiando o texto para análise...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        docs = text_splitter.create_documents([full_text])

        if not docs:
            return "O conteúdo da página era muito curto para gerar um resumo."

        print(f"Etapa 3: Iniciando a cadeia de resumo com {len(docs)} pedaços (chunks)...")
        try:
            summarize_chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
            # Usando .invoke() que é o método moderno do LangChain
            summary_output = summarize_chain.invoke({"input_documents": docs})
            summary = summary_output.get("output_text", "Não foi possível gerar o resumo.")
            print("--- [SummaryTool] Sucesso: Resumo gerado. ---")
            return summary
        except Exception as e:
            return f"Erro ao gerar o resumo com o LLM: {e}"

# Instância da ferramenta
summary_tool = SummaryTool()