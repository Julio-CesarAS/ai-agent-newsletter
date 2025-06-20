# src/tools/summary_tool.py
import os
from crewai_tools import BaseTool
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
import requests

class SummaryTool(BaseTool):
    name: str = "summary_tool" # Nome simplificado
    description: str = "Recebe uma URL de website, extrai seu conteúdo e gera um resumo conciso."

    def _run(self, url: str) -> str:
        print(f"\n--- [SummaryTool] Iniciando para a URL: {url} ---")
        llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
        
        print("Etapa 1: Raspando o conteúdo do site...")
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
            full_text = ' '.join([elem.get_text() for elem in text_elements])
            
            if not full_text.strip():
                return "Não foi possível extrair conteúdo textual significativo da URL."
        except Exception as e:
            return f"Erro ao acessar ou raspar a URL: {e}"

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