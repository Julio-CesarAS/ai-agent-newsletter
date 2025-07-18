# 📩 Newsletter AI - Sistema Automatizado de Newsletter sobre Tecnologia e UX Design

Um sistema completo de IA que utiliza múltiplos agentes inteligentes para automatizar a criação e envio de newsletters semanais sobre as últimas tendências em **Tecnologia** e **Design de Experiência do Usuário (UX)**.

---

## 🚀 Funcionalidades Principais

- **🔍 Busca Inteligente de Notícias**: Utiliza NewsAPI para encontrar as notícias mais relevantes e recentes
- **📝 Resumo Automatizado**: Web scraping robusto com IA para extrair e resumir conteúdo de artigos
- **🌐 Tradução Completa**: Tradução automática do inglês para português brasileiro usando GoogleTranslator
- **📧 Email HTML Profissional**: Geração e envio de newsletters com design responsivo via SendGrid
- **🛡️ Tratamento de Erros Robusto**: Sistema inteligente que lida com sites bloqueados e conteúdo inacessível
- **🤖 Arquitetura Multi-Agente**: Baseado no framework CrewAI para orquestração de agentes especializados

---

## 🛠️ Tecnologias Utilizadas

### **Framework e IA**
- **CrewAI**: Orquestração de agentes inteligentes
- **LangChain**: Processamento e resumo de texto
- **Groq API**: Acesso ao modelo Llama 3-8b-8192
- **GoogleTranslator**: Tradução automática para português

### **APIs e Serviços**
- **NewsAPI**: Busca de notícias em tempo real
- **SendGrid**: Envio profissional de emails
- **Beautiful Soup**: Web scraping avançado

### **Linguagem e Ambiente**
- **Python 3.11+**
- **uv**: Gerenciador de pacotes e ambiente virtual

---

## 📂 Estrutura do Projeto

```
📁 ai-agent-newsletter/
├── 📁 src/
│   ├── 📁 agents/
│   │   ├── __init__.py
│   │   └── news_agents.py          # Definição dos agentes (researcher, summarizer, editor)
│   ├── 📁 crew/
│   │   ├── __init__.py
│   │   └── news_crew.py            # Lógica principal de orquestração
│   ├── 📁 tasks/
│   │   ├── __init__.py
│   │   └── news_tasks.py           # Definição das tarefas dos agentes
│   ├── 📁 tools/
│   │   ├── __init__.py
│   │   ├── browser_tools.py        # Ferramenta de busca de notícias
│   │   ├── email_tools.py          # Ferramenta de envio de email
│   │   └── summary_tool.py         # Ferramenta de resumo e web scraping
│   ├── 📁 templates/
│   │   └── newsletter.html         # Template HTML da newsletter
│   └── main.py                     # Ponto de entrada da aplicação
├── 📁 ui/
│   └── app.py                      # Interface de usuário (Streamlit)
├── 📁 scripts/
│   └── setup_database.sql          # Scripts de configuração do banco
├── .env                            # Variáveis de ambiente (não commitado)
├── requirements.txt                # Dependências do projeto
└── README.md                       # Este arquivo
```

---

## ⚙️ Configuração e Instalação

### **Pré-requisitos**
- Python 3.11 ou superior
- `uv` instalado (`pip install uv`)

### **1. Clone o Repositório**
```bash
git clone https://github.com/Julio-CesarAS/ai-agent-newsletter.git
cd ai-agent-newsletter
```

### **2. Configure o Ambiente Virtual**
```bash
# Criar ambiente virtual
uv venv -p python3.11

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### **3. Instale as Dependências**
```bash
uv pip install -r requirements.txt
```

### **4. Configure as Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
# NewsAPI - Obtenha em https://newsapi.org/
NEWSAPI_KEY=sua_chave_newsapi_aqui

# Groq API - Obtenha em https://console.groq.com/
GROQ_API_KEY=sua_chave_groq_aqui

# SendGrid - Obtenha em https://app.sendgrid.com/
SENDGRID_API_KEY=sua_chave_sendgrid_aqui
SENDER_EMAIL=seu_email_verificado_no_sendgrid
```

---

## 🚀 Como Usar

### **Execução Básica**
```bash
python -m src.main
```

O sistema solicitará o email do destinatário e executará automaticamente:

1. **Busca de Notícias**: Encontra artigos sobre tecnologia e UX design
2. **Processamento**: Filtra e processa os resultados
3. **Resumo**: Extrai e resume o conteúdo dos artigos
4. **Tradução**: Converte todo o conteúdo para português brasileiro
5. **Envio**: Gera HTML profissional e envia por email

### **Execução com Interface Web**
```bash
cd ui
streamlit run app.py
```

---

## 🔧 Funcionalidades Avançadas

### **Sistema de Tratamento de Erros**
- **Sites Bloqueados**: Detecta e pula automaticamente sites que bloqueiam bots (erro 403/420/429)
- **Conteúdo Inacessível**: Filtra artigos sem conteúdo válido
- **Retry Logic**: Implementa tentativas automáticas com delays para rate limiting
- **Headers Personalizados**: Simula navegadores reais para melhor acesso

### **Web Scraping Inteligente**
- **Múltiplos Seletores**: Tenta diferentes estratégias para extrair conteúdo
- **Limpeza Automática**: Remove scripts, estilos e elementos irrelevantes
- **Timeout Configurável**: Evita travamentos em sites lentos

### **Tradução Robusta**
- **Chunking Inteligente**: Divide textos longos para melhor qualidade
- **Fallback**: Mantém texto original se tradução falhar
- **Contexto Preservado**: Mantém formatação e estrutura do conteúdo

---

## 📊 Exemplo de Saída

O sistema gera newsletters HTML profissionais com:

- **Cabeçalho personalizado** com título em português
- **Seções organizadas** por categoria (Tecnologia e UX Design)
- **Links funcionais** para artigos originais
- **Design responsivo** compatível com todos os clientes de email
- **Formatação profissional** com cores e tipografia otimizadas

---

## 🔑 APIs Necessárias

| Serviço | Finalidade | Link de Cadastro | Plano Gratuito |
|---------|------------|------------------|----------------|
| **NewsAPI** | Busca de notícias | [newsapi.org](https://newsapi.org/) | ✅ 1000 requests/mês |
| **Groq** | Modelo de IA (Llama 3) | [console.groq.com](https://console.groq.com/) | ✅ Gratuito com limites |
| **SendGrid** | Envio de emails | [sendgrid.com](https://sendgrid.com/) | ✅ 100 emails/dia |

---

## 🧠 Arquitetura dos Agentes

### **Researcher Agent**
- **Função**: Busca e coleta notícias relevantes
- **Ferramentas**: NewsAPI integration
- **Especialização**: Filtrar conteúdo por relevância e qualidade

### **Summarizer Agent**
- **Função**: Extrai e resume conteúdo de artigos
- **Ferramentas**: Web scraping + LangChain
- **Especialização**: Processamento de texto e sumarização

### **Editor Agent**
- **Função**: Formatação e organização final
- **Ferramentas**: Template HTML + GoogleTranslator
- **Especialização**: Estruturação de conteúdo e tradução

---

## 🚦 Status do Projeto

- ✅ **Core MVP**: Funcional e testado
- ✅ **Tradução Completa**: Implementada
- ✅ **Web Scraping Robusto**: Implementado
- ✅ **Tratamento de Erros**: Implementado
- ✅ **HTML Profissional**: Implementado
- 🔄 **Interface Web**: Em desenvolvimento
- 🔄 **Banco de Dados**: Planejado
- 🔄 **Agendamento**: Planejado

---

## 🛣️ Roadmap

### **Próximas Funcionalidades**
- [ ] **Sistema de Assinantes**: Banco de dados com lista de emails
- [ ] **Interface Web Completa**: Dashboard para gerenciar newsletters
- [ ] **Agendamento Automático**: Cron jobs para envio programado
- [ ] **Analytics**: Métricas de abertura e cliques
- [ ] **Personalização**: Templates customizáveis
- [ ] **API REST**: Endpoints para integração externa

### **Melhorias Técnicas**
- [ ] **Cache de Artigos**: Evitar reprocessamento
- [ ] **Paralelização**: Processamento simultâneo de artigos
- [ ] **Logs Estruturados**: Sistema de logging avançado
- [ ] **Testes Automatizados**: Cobertura completa de testes
- [ ] **Docker**: Containerização da aplicação

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais e pessoais.

---

## 👨‍💻 Autor

**Julio Cesar** - [GitHub](https://github.com/Julio-CesarAS)
                  [LinkedIn](https://www.linkedin.com/in/juliocesar-productdesigner/)      

---

## 🙏 Agradecimentos

- **CrewAI Team** - Framework de agentes inteligentes
- **Groq** - Acesso gratuito ao Llama 3
- **SendGrid** - Plataforma confiável de email
- **NewsAPI** - Fonte de notícias em tempo real

---

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma [Issue](https://github.com/Julio-CesarAS/ai-agent-newsletter/issues)
- Entre em contato via [LinkedIn](https://linkedin.com/in/julio-cesar-as)

---

<p align="center">
  <strong>Construído com ❤️ e IA para automatizar o futuro das newsletters</strong>
</p>
