# src/agents/news_agents.py
import os
from crewai import Agent
from langchain_groq import ChatGroq
from textwrap import dedent

class NewsAgents:
    def __init__(self):
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def make_researcher_agent(self) -> Agent:
        return Agent(
            role="Pesquisador de Notícias Sênior",
            goal="Encontrar as 6 URLs das notícias mais relevantes sobre tecnologia e design.",
            backstory="Especialista em encontrar artigos online de fontes confiáveis sobre tópicos específicos.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def make_summarizer_agent(self) -> Agent:
        return Agent(
            role="Resumidor de Artigos Profissional",
            goal="Para cada URL recebida, criar um resumo conciso em inglês usando a ferramenta de resumo.",
            backstory="Você é perito em usar ferramentas para extrair e resumir o conteúdo de páginas da web.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def make_editor_agent(self) -> Agent:
        return Agent(
            role="Editor e Tradutor de Newsletter",
            goal="Traduzir resumos de notícias para o Português do Brasil e formatá-los em uma newsletter coesa.",
            backstory="Um editor bilíngue com talento para criar conteúdo envolvente e bem formatado para o público brasileiro.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )