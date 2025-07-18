# src/crew/news_crew.py
from crewai import Crew, Process, Task
from dotenv import load_dotenv
from textwrap import dedent
from deep_translator import GoogleTranslator
load_dotenv()

from src.agents.news_agents import NewsAgents
from src.tools.browser_tools import news_search_tool
from src.tools.email_tools import email_tool
from src.tools.summary_tool import summary_tool
import json
import re # Precisamos do 're' para a extração do JSON

class NewsCrew:
    def __init__(self, recipient_email: str):
        self.recipient_email = recipient_email
        self.agents = NewsAgents()
        self.tools = {
            "email": email_tool,
            "browser": news_search_tool,
            "summary": summary_tool
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

    def _translate_text(self, text: str) -> str:
        """Traduz texto do inglês para português brasileiro."""
        try:
            translator = GoogleTranslator(source='en', target='pt')
            # Dividir texto longo em chunks menores para evitar limite da API
            if len(text) > 500:
                # Dividir por sentenças
                sentences = text.split('. ')
                translated_sentences = []
                for sentence in sentences:
                    if sentence.strip():
                        translated = translator.translate(sentence.strip())
                        translated_sentences.append(translated)
                return '. '.join(translated_sentences)
            else:
                return translator.translate(text)
        except Exception as e:
            print(f"⚠️  Erro na tradução: {e}")
            return text  # Retorna texto original se tradução falhar

    def run(self):
        researcher = self.agents.make_researcher_agent()
        summarizer = self.agents.make_summarizer_agent()
        editor = self.agents.make_editor_agent()

        # --- ETAPA 1: PESQUISA DIRECIONADA ---
        print("--- [Etapa 1/5] Pesquisando notícias... ---")
        
        # Buscar notícias diretamente usando as funções
        print("🔍 Buscando notícias sobre tecnologia...")
        tech_results_str = self.tools['browser']._run("technology trends")
        print("🔍 Buscando notícias sobre UX design...")
        ux_results_str = self.tools['browser']._run("user experience design UX")
        
        # --- ETAPA 2: PROCESSAMENTO DOS RESULTADOS ---
        print("\n--- [Etapa 2/5] Processando resultados da pesquisa... ---")
        
        # Usando a função auxiliar para extrair o JSON de forma segura da resposta
        tech_articles = self._extract_json_from_string(tech_results_str)
        ux_articles = self._extract_json_from_string(ux_results_str)
        
        print(f"📰 Encontradas {len(tech_articles)} notícias de tecnologia:")
        for i, article in enumerate(tech_articles, 1):
            print(f"  {i}. {article.get('title', 'Título não disponível')}")
            
        print(f"📰 Encontradas {len(ux_articles)} notícias de UX:")
        for i, article in enumerate(ux_articles, 1):
            print(f"  {i}. {article.get('title', 'Título não disponível')}")
        
        articles = tech_articles + ux_articles

        if not articles:
            print("❌ Nenhum artigo foi encontrado ou processado. Encerrando.")
            return

        print(f"\n✅ {len(articles)} artigos encontrados e processados com sucesso.")

        # --- ETAPA 3: RESUMO DOS ARTIGOS (COM TRATAMENTO DE ERRO) ---
        print("\n--- [Etapa 3/5] Resumindo artigos... ---")
        summaries = []
        for i, article in enumerate(articles):
            print(f"\n📝 Resumindo artigo {i+1}/{len(articles)}:")
            print(f"   Título: {article['title']}")
            print(f"   URL: {article['url']}")
            try:
                # Usar a ferramenta de resumo diretamente
                summary = self.tools['summary']._run(article['url'])
                category = "tech" if i < len(tech_articles) else "ux"
                
                # Verificar se o resumo contém erro
                if summary.startswith("Erro") or summary.startswith("Site") or "indisponível" in summary.lower():
                    print(f"   ⚠️  Artigo inacessível: {summary}")
                    print(f"   ⏭️  Pulando artigo...")
                    continue  # Pular este artigo completamente
                else:
                    summaries.append({"title": article['title'], "summary": summary, "url": article['url'], "category": category})
                    print(f"   ✅ Resumo gerado com sucesso!")
                    
            except Exception as e:
                print(f"   ❌ ERRO inesperado ao resumir o artigo. Erro: {e}")
                print(f"   ⏭️  Pulando artigo...")
                continue
        
        if not summaries:
            print("❌ Nenhum resumo pode ser gerado. Encerrando.")
            return

        # Contar resumos válidos
        valid_summaries = [s for s in summaries if s['summary'] != "Não foi possível gerar o resumo para este artigo."]
        print(f"\n📊 Resumos gerados: {len(valid_summaries)}/{len(summaries)} artigos")

        # --- ETAPA 4: TRADUÇÃO E EDIÇÃO ---
        print("\n--- [Etapa 4/5] Traduzindo títulos e resumos para português... ---")
        
        if not summaries:
            print("❌ Nenhum artigo válido para traduzir. Encerrando.")
            return "Nenhum artigo válido foi encontrado para a newsletter."
        
        # Traduzir todos os títulos e resumos
        translated_summaries = []
        for i, summary in enumerate(summaries):
            print(f"🌐 Traduzindo artigo {i+1}/{len(summaries)}: {summary['title'][:50]}...")
            
            # Traduzir título
            translated_title = self._translate_text(summary['title'])
            
            # Traduzir resumo
            translated_summary_text = self._translate_text(summary['summary'])
            
            translated_summaries.append({
                'title': translated_title,
                'summary': translated_summary_text,
                'url': summary['url'],
                'category': summary['category']
            })
            print(f"   ✅ Tradução concluída!")
        
        # Atualizar summaries com versões traduzidas
        summaries = translated_summaries
        
        print(f"📰 Newsletter preparada com {len(summaries)} artigos traduzidos.")

        # --- ETAPA 5: GERAÇÃO DO HTML E ENVIO ---
        print("\n--- [Etapa 5/5] Montando o HTML e Enviando a Newsletter Final ---")
        
        html_body_parts = []
        
        # Usar todos os resumos (agora todos são válidos)
        all_summaries = summaries

        # Separa por categoria para a montagem final
        tech_articles_final = [s for s in all_summaries if s['category'] == 'tech']
        ux_articles_final = [s for s in all_summaries if s['category'] == 'ux']
        
        print(f"🏗️  Montando HTML:")
        print(f"   - {len(tech_articles_final)} artigos de tecnologia")
        print(f"   - {len(ux_articles_final)} artigos de UX design")
        
        # Adiciona a seção de Tecnologia
        for article in tech_articles_final:
             html_body_parts.append(f"""<tr><td style="padding: 15px 0; border-bottom: 1px solid #eeeeee;"><a href="{article['url']}" style="text-decoration: none;"><h3 style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: #363737; margin-bottom: 5px;">{article['title']}</h3></a><p style="font-size: 16px; color: #555555; line-height: 1.5; margin-top: 5px;">{article['summary']}</p></td></tr>""")
        
        # Adiciona a seção de UX Design
        if ux_articles_final:
            html_body_parts.insert(len(tech_articles_final), '<tr><td style="padding: 20px 0 10px 0;"><h2 style="color: #363737; border-bottom: 2px solid #363737; padding-bottom: 5px;">Notícias de UX Design</h2></td></tr>')
        for article in ux_articles_final:
             html_body_parts.append(f"""<tr><td style="padding: 15px 0; border-bottom: 1px solid #eeeeee;"><a href="{article['url']}" style="text-decoration: none;"><h3 style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: #363737; margin-bottom: 5px;">{article['title']}</h3></a><p style="font-size: 16px; color: #555555; line-height: 1.5; margin-top: 5px;">{article['summary']}</p></td></tr>""")

        newsletter_html_body = "".join(html_body_parts)
        
        # Adiciona o cabeçalho de Tecnologia se houver notícias de tecnologia
        if tech_articles_final:
            newsletter_html_body = '<tr><td style="padding: 10px 0;"><h2 style="color: #363737; border-bottom: 2px solid #363737; padding-bottom: 5px;">Notícias de Tecnologia</h2></td></tr>' + newsletter_html_body

        html_content = f"""
        <html><head><style>body {{ font-family: Arial, sans-serif; }}</style></head><body>
        <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
        <table width="40%" border="0" cellspacing="0" cellpadding="20" style="max-width: 600px; min-width: 400px; border-collapse: collapse;">
            <tr><td align="center" style="padding: 20px 0;"><h1 style="font-size: 28px; color: #363737;">Seu Resumo Semanal sobre Design e Tecnologia</h1></td></tr>
            {newsletter_html_body}
        </table></td></tr></table></body></html>
        """
        
        print("📧 Enviando newsletter por e-mail...")
        email_function = self.tools['email']
        email_result = email_function._run(recipient_email=self.recipient_email, content=html_content)
        print(f"📨 {email_result}")
        
        return f"✅ Processo concluído. Newsletter gerada com {len(all_summaries)} artigos e enviada com sucesso."