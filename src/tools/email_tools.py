# src/tools/email_tools.py
import os
from crewai_tools import BaseTool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailTools(BaseTool):
    name: str = "email_tool"
    description: str = "Envia um e-mail com a newsletter finalizada para um destinatário usando o SendGrid."

    def _run(self, recipient_email: str, content: str) -> str:
        sender_email = os.getenv("SENDER_EMAIL")
        api_key = os.getenv("SENDGRID_API_KEY")

        if not all([sender_email, api_key]):
            return "Erro: Variáveis de ambiente SENDER_EMAIL e SENDGRID_API_KEY devem estar configuradas."

        # A mudança crítica está aqui: o conteúdo agora é tratado como 'html_content'
        message = Mail(
            from_email=sender_email,
            to_emails=recipient_email,
            subject="O seu resumo semanal sobre Design e Tecnologia", # Título do e-mail atualizado
            html_content=content # Usando html_content em vez de plain_text
        )

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            if response.status_code >= 200 and response.status_code < 300:
                return f"Newsletter enviada com sucesso para {recipient_email}."
            else:
                return f"Falha ao enviar e-mail via SendGrid. Status: {response.status_code}. Detalhes: {response.body}"
        except Exception as e:
            return f"Uma exceção ocorreu ao enviar o e-mail via SendGrid: {e}"