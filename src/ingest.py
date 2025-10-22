import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()


required_vars = ["GOOGLE_API_KEY", "PGVECTOR_URL", "GEMINI_VECTOR_COLLECTION"]
for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Environment variable {var} is not set")

def ingest_pdf():
    """
    Ingere o PDF no banco de dados vetorial
    """
    print("Iniciando processo de ingestão do PDF...")
    
    
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / "document.pdf"
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
    
    print(f"Carregando PDF: {pdf_path}")
    
    
    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()
    
    if not docs:
        raise ValueError("Nenhum documento foi carregado do PDF")
    
    print(f"Documento carregado com {len(docs)} páginas")
    
    print("Dividindo documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True
    )
    
    splits = text_splitter.split_documents(docs)
    
    if not splits:
        raise ValueError("Nenhum chunk foi gerado")
    
    print(f"Gerados {len(splits)} chunks")
    
    
    enriched_docs = []
    for i, doc in enumerate(splits):
        cleaned_metadata = {k: v for k, v in doc.metadata.items() if v not in ("", None)}
        new_doc = Document(
            page_content=doc.page_content,
            metadata=cleaned_metadata
        )
        enriched_docs.append(new_doc)
    
    
    ids = [f"doc-{i}" for i in range(len(enriched_docs))]
    
    
    print("Configurando embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
    )
    
    
    print("Conectando ao banco de dados vetorial...")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("GEMINI_VECTOR_COLLECTION", "default_gemini_collection"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    
    
    print("Salvando documentos no banco de dados...")
    vector_store.add_documents(documents=enriched_docs, ids=ids)
    
    print("Ingestão concluída com sucesso!")
    print(f"Total de documentos salvos: {len(enriched_docs)}")

if __name__ == "__main__":
    try:
        ingest_pdf()
    except Exception as e:
        print(f"Erro durante a ingestão: {e}")
        exit(1)