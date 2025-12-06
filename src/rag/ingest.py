"""
Data Ingestion Script - Load PDF documents to vector database
Uses local HuggingFace embeddings to avoid API quota limits
"""
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Get project root: src/rag -> src -> project_root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_DIR = os.path.join(PROJECT_ROOT, "chroma_db")

def ingest_data():
    documents = []
    
    # Load Bitcoin PDF
    pdf_path = os.path.join(DATA_DIR, "bitcoin.pdf")
    print(f"Looking for PDF at: {pdf_path}")
    if os.path.exists(pdf_path):
        print("Loading Bitcoin PDF...")
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    
    # Load Ethereum Whitepaper (Text)
    eth_path = os.path.join(DATA_DIR, "ethereum.md")
    if os.path.exists(eth_path):
        print("Loading Ethereum Whitepaper...")
        loader = TextLoader(eth_path, encoding="utf-8")
        documents.extend(loader.load())

    if not documents:
        print("No documents found to ingest.")
        return

    print(f"Loaded {len(documents)} pages/documents.")

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # Use local HuggingFace embeddings (no API quota issues)
    print("Using local HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Embed and store
    print("Embedding and storing in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Ingestion complete!")
    print(f"Vector database saved to: {DB_DIR}")

if __name__ == "__main__":
    ingest_data()
