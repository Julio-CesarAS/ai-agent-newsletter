# src/tasks/news_tasks.py
from crewai import Task
from textwrap import dedent

class NewsTasks:
    # A tarefa agora é apenas passar a URL para a ferramenta, sem lógica complexa.
    def make_summarization_task(self, agent, article):
        return Task(
            description=f"Resuma o conteúdo da seguinte URL: {article['url']}",
            expected_output="Um resumo conciso em inglês do artigo.",
            agent=agent,
            # Passando o artigo específico como contexto para esta tarefa atômica
            context=[Task(description=f"URL e Título do Artigo: {article['title']}\n{article['url']}", expected_output="")]
        )
    
    # As outras tarefas permanecem, mas a de edição será usada de outra forma.
    # O código principal em news_crew.py orquestrará o fluxo.