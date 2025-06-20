
# 📩 Newsletter de IA sobre Design & Tecnologia

Este projeto utiliza um grupo de agentes de Inteligência Artificial, construído com o framework **CrewAI**, para automatizar completamente a criação e o envio de uma newsletter semanal sobre as últimas novidades em Tecnologia e Design de Experiência do Usuário (UX).

---

## 🎯 Objetivo

Criar um sistema autônomo que, a cada 3 dias, busca as notícias mais recentes e relevantes em fontes de alta credibilidade, resume o conteúdo de cada artigo, traduz para o Português do Brasil, formata em um e-mail HTML profissional e o envia para uma lista de assinantes.

---

## ✨ Funcionalidades Principais

- **Busca de Notícias Direcionada:** Os agentes pesquisam ativamente por notícias sobre _tendências de tecnologia_ e _design de experiência do usuário_.
- **Processamento Robusto de Conteúdo:** Arquitetura _Map-Reduce_ para resumir artigos longos sem estourar o limite de tokens da API do LLM.
- **Tratamento Inteligente de Erros:** Resiliência para ignorar artigos inacessíveis (links quebrados, sites bloqueados) e continuar com os demais.
- **Tradução por IA:** O conteúdo é traduzido para um português fluente e natural.
- **Geração de E-mail em HTML:** Uso de templates Jinja2 para criar uma newsletter com formatação profissional (fontes, cores, layout centralizado e títulos com hyperlinks).
- **Envio Automatizado:** Integração com SendGrid para garantir alta entregabilidade.

---

## 🛠️ Tecnologias Utilizadas

- **Framework de Agentes IA:** CrewAI
- **Modelo de Linguagem (LLM):** Llama 3 (via API da Groq)
- **Serviços de API:**
  - **NewsAPI:** Busca de notícias
  - **Groq:** Acesso ao LLM
  - **SendGrid:** Envio de e-mails
- **Bibliotecas Chave (Python):**
  - `crewai`, `crewai-tools`
  - `langchain`, `langchain-groq`, `langchain-text-splitters`
  - `python-dotenv`
  - `requests`, `beautifulsoup4`
  - `Jinja2`
  - `uv` (para gerenciamento de ambiente e pacotes)

---

## 📂 Estrutura do Projeto

```
/newsletter-crew/
├── /src/
│   ├── /agents/
│   │    └── news_agents.py
│   ├── /tools/
│   │    ├── browser_tools.py
│   │    ├── email_tools.py
│   │    └── summary_tool.py
│   ├── /crew/
│   │    └── news_crew.py
│   └── main.py
├── /templates/
│   └── newsletter.html
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Configuração e Instalação

### Pré-requisitos

- Python 3.11+
- `uv` instalado (`pip install uv`)

### Passo 1 - Clone o Repositório

```bash
git clone https://github.com/seu-usuario/newsletter-crew.git
cd newsletter-crew
```

### Passo 2 - Crie e Ative o Ambiente Virtual

```bash
# Criar ambiente
uv venv -p python3.11

# Ativar ambiente
source .venv/bin/activate
```

### Passo 3 - Instale as Dependências

```bash
uv pip install -r requirements.txt
```

### Passo 4 - Configure as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:
OBS: Você pode usar o aquivo ".env.example" na raiz do seu projeto, basta deletar o .example do nome do arquivo e adicionar as cerdencias necessárias para o projeto, conforme solicitado pelo aquivo.

```
# .env

# Chave da API para buscar notícias (obtenha em https://newsapi.org/)
NEWSAPI_KEY=SUA_CHAVE_AQUI

# Chave da API do Groq (obtenha em https://console.groq.com/)
GROQ_API_KEY=SUA_CHAVE_AQUI

# --- Configuração do SendGrid ---
# Chave da API (obtenha em https://app.sendgrid.com/)
SENDGRID_API_KEY=SUA_CHAVE_AQUI

# E-mail verificado no SendGrid
SENDER_EMAIL=SEU_EMAIL_VERIFICADO_AQUI
```

---

### ▶️ Como Executar

Com o ambiente ativo e o `.env` configurado, execute o script principal:

```bash
python -m src.main
```

O programa solicitará o e-mail do destinatário e iniciará o processo de criação e envio da newsletter.

---

## 🔮 Próximos Passos

- [ ] **Integração com Banco de Dados:** Buscar lista de assinantes diretamente de uma base como o Supabase.
- [ ] **Interface de Interface de Usuário (UI):** Criar uma página web com Flask ou Streamlit para inscrição de novos usuários.
- [ ] **Agendamento de Execução:** Configurar um Cron Job para rodar o `main.py` automaticamente a cada 3 dias.

---

## ✅ Status Atual

Projeto em desenvolvimento inicial (MVP funcional).

---

## 📌 Observação

> Caso queira testar o envio, use um endereço de e-mail verificado no painel da SendGrid para evitar bloqueios de API.
