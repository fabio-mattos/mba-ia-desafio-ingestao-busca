
import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def format_docs(docs):
    """Formata os documentos recuperados em uma string única"""
    return "\n\n".join([f"Documento {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

def search_prompt():
    """
    Configura e retorna a chain de busca RAG
    """
    try:
        required_vars = ["GOOGLE_API_KEY", "PGVECTOR_URL", "GEMINI_VECTOR_COLLECTION"]
        for var in required_vars:
            if not os.getenv(var):
                print(f"Variável de ambiente {var} não está configurada")
                return None
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
        )
        
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("GEMINI_VECTOR_COLLECTION", "default_gemini_collection"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        
        # Configurar o modelo de linguagem da llm
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0
        )
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        
        rag_chain = (
            {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain
        
    except Exception as e:
        print(f"Erro ao configurar a busca: {e}")
        return None

def search_documents(query):
    """
    Busca documentos relevantes para uma query específica
    """
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
        )
        
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("GEMINI_VECTOR_COLLECTION", "default_gemini_collection"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
        
        results = vector_store.similarity_search_with_score(query, k=10)
        
        return results
        
    except Exception as e:
        print(f"Erro ao buscar documentos: {e}")
        return []