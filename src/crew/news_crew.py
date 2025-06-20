# src/crew/news_crew.py
from crewai import Crew, Process, Task
from dotenv import load_dotenv
from textwrap import dedent
load_dotenv()

from src.agents.news_agents import NewsAgents
from src.tools.browser_tools import BrowserTool
from src.tools.email_tools import EmailTools
from src.tools.summary_tool import SummaryTool
import json
import re # Precisamos do 're' para a extração do JSON

class NewsCrew:
    def __init__(self, recipient_email: str):
        self.recipient_email = recipient_email
        self.agents = NewsAgents()
        self.tools = {
            "email": EmailTools(),
            "browser": BrowserTool(),
            "summary": SummaryTool()
        }

    def _extract_json_from_string(self, text: str) -> list:
        # Esta função auxiliar encontra e extrai a primeira string JSON válida do texto
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return []
        return []

    def run(self):
        researcher = self.agents.make_researcher_agent()
        summarizer = self.agents.make_summarizer_agent()
        editor = self.agents.make_editor_agent()

        researcher.tools = [self.tools['browser']]
        summarizer.tools = [self.tools['summary']]
        
        # --- ETAPA 1: PESQUISA DIRECIONADA ---
        print("--- [Etapa 1/5] Pesquisando notícias... ---")
        tech_task = Task(description="Buscar 3 notícias sobre 'tendências de tecnologia'", expected_output="Uma string JSON de uma lista de artigos.", agent=researcher)
        ux_task = Task(description="Buscar 3 notícias sobre 'design de experiência do usuário UX'", expected_output="Uma string JSON de uma lista de artigos.", agent=researcher)

        tech_results_str = tech_task.execute()
        ux_results_str = ux_task.execute()
        
        # --- ETAPA 2: PROCESSAMENTO DOS RESULTADOS ---
        print("\n--- [Etapa 2/5] Processando resultados da pesquisa... ---")
        
        # --- CORREÇÃO AQUI ---
        # Usando a função auxiliar para extrair o JSON de forma segura da resposta do agente
        tech_articles = self._extract_json_from_string(tech_results_str)
        ux_articles = self._extract_json_from_string(ux_results_str)
        
        articles = tech_articles + ux_articles

        if not articles:
            print("Nenhum artigo foi encontrado ou processado. Encerrando.")
            return

        print(f"{len(articles)} artigos encontrados e processados com sucesso.")

        # --- ETAPA 3: RESUMO DOS ARTIGOS (COM TRATAMENTO DE ERRO) ---
        print("\n--- [Etapa 3/5] Resumindo artigos... ---")
        summaries = []
        for i, article in enumerate(articles):
            print(f"\nResumindo artigo {i+1}/{len(articles)}: {article['title']}")
            summarization_task = Task(
                description=f"Use a ferramenta de resumo para o artigo na URL: {article['url']}",
                expected_output="Um resumo conciso do artigo em inglês.",
                agent=summarizer,
                tools=[self.tools['summary']]
            )
            try:
                summary = summarization_task.execute()
                category = "tech" if i < len(tech_articles) else "ux"
                summaries.append({"title": article['title'], "summary": summary, "url": article['url'], "category": category})
            except Exception as e:
                print(f"!!! ERRO ao resumir o artigo '{article['title']}'. Pulando. Erro: {e}")
                category = "tech" if i < len(tech_articles) else "ux"
                summaries.append({"title": article['title'], "summary": "Não foi possível gerar o resumo para este artigo.", "url": article['url'], "category": category})
                continue
        
        if not summaries:
            print("Nenhum resumo pode ser gerado. Encerrando.")
            return

        # --- ETAPA 4: TRADUÇÃO E EDIÇÃO ---
        print("\n--- [Etapa 4/5] Editando e traduzindo a newsletter... ---")
        editing_task = Task(
            description=dedent(f"""
                Traduza a lista de títulos e resumos abaixo para o Português do Brasil e formate em uma newsletter.
                DADOS: {str(summaries)}
                REGRAS:
                - Traduza cada 'title' e 'summary'.
                - Formate a saída como uma única string de texto.
                - Formato: **Título em Português**\nResumo em português.\n\n
            """),
            expected_output="O texto final da newsletter em português, pronto para ser enviado.",
            agent=editor,
        )
        final_newsletter_text = editing_task.execute()

        # --- ETAPA 5: GERAÇÃO DO HTML E ENVIO ---
        print("\n--- [Etapa 5/5] Montando o HTML e Enviando a Newsletter Final ---")
        
        html_body_parts = []
        news_blocks = [block for block in final_newsletter_text.strip().split('\n\n') if block]
        
        translated_articles_map = {block.split('\n', 1)[0].replace('**', '').strip(): block.split('\n', 1)[1].strip() if len(block.split('\n', 1)) > 1 else "Resumo não disponível." for block in news_blocks}

        all_summaries = [s for s in summaries if s['summary'] != "Não foi possível gerar o resumo para este artigo."]

        # Separa por categoria para a montagem final
        tech_articles_final = [s for s in all_summaries if s['category'] == 'tech']
        ux_articles_final = [s for s in all_summaries if s['category'] == 'ux']
        
        # Adiciona a seção de Tecnologia
        for article in tech_articles_final:
             translated_title = next((t for t in translated_articles_map if article['title'] in t or t in article['title']), article['title'])
             translated_summary = translated_articles_map.get(translated_title, article['summary'])
             html_body_parts.append(f"""<tr><td style="padding: 15px 0; border-bottom: 1px solid #eeeeee;"><a href="{article['url']}" style="text-decoration: none;"><h3 style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: #363737; margin-bottom: 5px;">{translated_title}</h3></a><p style="font-size: 16px; color: #555555; line-height: 1.5; margin-top: 5px;">{translated_summary}</p></td></tr>""")
        
        # Adiciona a seção de UX Design
        if ux_articles_final:
            html_body_parts.insert(len(tech_articles_final), '<tr><td style="padding: 20px 0 10px 0;"><h2 style="color: #363737; border-bottom: 2px solid #363737; padding-bottom: 5px;">Notícias de UX Design</h2></td></tr>')
        for article in ux_articles_final:
             translated_title = next((t for t in translated_articles_map if article['title'] in t or t in article['title']), article['title'])
             translated_summary = translated_articles_map.get(translated_title, article['summary'])
             html_body_parts.append(f"""<tr><td style="padding: 15px 0; border-bottom: 1px solid #eeeeee;"><a href="{article['url']}" style="text-decoration: none;"><h3 style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: #363737; margin-bottom: 5px;">{translated_title}</h3></a><p style="font-size: 16px; color: #555555; line-height: 1.5; margin-top: 5px;">{translated_summary}</p></td></tr>""")

        newsletter_html_body = "".join(html_body_parts)
        
        # Adiciona o cabeçalho de Tecnologia se houver notícias de tecnologia
        if tech_articles_final:
            newsletter_html_body = '<tr><td style="padding: 10px 0;"><h2 style="color: #363737; border-bottom: 2px solid #363737; padding-bottom: 5px;">Notícias de Tecnologia</h2></td></tr>' + newsletter_html_body

        html_content = f"""
        <html><head><style>body {{ font-family: Arial, sans-serif; }}</style></head><body>
        <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
        <table width="40%" border="0" cellspacing="0" cellpadding="20" style="max-width: 600px; min-width: 400px; border-collapse: collapse;">
            <tr><td align="center" style="padding: 20px 0;"><h1 style="font-size: 28px; color: #363737;">O seu resumo semanal sobre Design e Tecnologia</h1></td></tr>
            {newsletter_html_body}
        </table></td></tr></table></body></html>
        """
        
        email_tool = self.tools['email']
        email_result = email_tool.run(recipient_email=self.recipient_email, content=html_content)
        print(email_result)
        
        return "Processo concluído. Newsletter gerada e enviada com sucesso."