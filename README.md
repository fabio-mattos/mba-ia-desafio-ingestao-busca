# Ingestão e Busca Semântica com LangChain e Postgres

Desafio Tecnico - MBA IA Engenharia de Software - FullCycle\
Aluno: Fábio Celso de Mattos\
Turma: Setembro 2025

---

Objetivos do Desafio:
Sistema de pergunta e resposta baseado em documentos PDF usando LangChain, PostgreSQL com pgVector e Google Gemini.

## 🚀 Funcionalidades

- **Ingestão**: Lê arquivos PDF e salva em banco vetorial PostgreSQL
- **Busca Semântica**: Permite fazer perguntas via CLI sobre o conteúdo do PDF
- **Respostas Contextualizadas**: Responde apenas com base no conteúdo do documento

## 🛠️ Tecnologias

- **Python 3.9+**
- **LangChain** - Framework para aplicações com LLM
- **PostgreSQL + pgVector** - Banco de dados vetorial
- **Google Gemini** - Embeddings e LLM
- **Docker & Docker Compose** - Containerização do banco

## 📋 Pré-requisitos

1. **Python 3.9+** instalado
2. **Docker e Docker Compose** instalados
   Link como instalar Docker e Doker Compose
   https://www.docker.com/products/docker-desktop/

3. **API Key do Google Gemini**
   <br>OBS: Para gerar a API Key do Google Gemini <br>acesse o site:
   https://aistudio.google.com/app/apikey

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/fabio-mattos/mba-ia-desafio-ingestao-busca
cd mba-ia-desafio-ingestao-busca
```

### 2. Configure as variáveis de ambiente

Configure sua API Key no arquivo `.env`:

```env
GOOGLE_API_KEY=[troque_esse_testo_pela_sua_api_key]
GEMINI_EMBEDDING_MODEL=models/embedding-001
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
GEMINI_VECTOR_COLLECTION=default_gemini_collection
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
pip install python-dotenv
pip install langchain langchain-community langchain-core
```

## 🚀 Execução

### 1. Subir o banco de dados PostgreSQL

```bash
docker compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente.

### 2. Executar a ingestão do PDF

```bash
python src/ingest.py
```

Este comando irá:

- Carregar o arquivo `document.pdf`
- Dividir em chunks de 1000 caracteres (overlap de 150)
- Gerar embeddings usando Google Gemini
- Salvar no banco vetorial PostgreSQL

### 3. Iniciar o chat

```bash
python src/chat.py
```

## 💬 Exemplo de Uso

```
🤖 Chat com Documentos - Sistema RAG
==================================================

Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
==================================================
RESPOSTA: O faturamento foi de 10 milhões de reais.
==================================================

Faça sua pergunta: Quantos clientes temos em 2024?
PERGUNTA: Quantos clientes temos em 2024?
==================================================
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
==================================================
```

## 📁 Estrutura do Projeto

```
├── docker-compose.yml     # Configuração do PostgreSQL + pgVector
├── requirements.txt       # Dependências Python
├── .env                  # Variáveis de ambiente
├── document.pdf          # PDF para ingestão
├── README.md             # Este arquivo
└── src/
    ├── ingest.py         # Script de ingestão do PDF
    ├── search.py         # Lógica de busca semântica
    └── chat.py           # Interface CLI para chat
```

## 🔧 Parâmetros de Configuração

### Ingestão

- **Chunk size**: 1000 caracteres
- **Chunk overlap**: 150 caracteres
- **Embedding model**: `models/embedding-001` (Google Gemini)

### Busca

- **Número de documentos recuperados**: 10 (k=10)
- **LLM**: `gemini-1.5-flash`
- **Temperature**: 0 (respostas determinísticas)
