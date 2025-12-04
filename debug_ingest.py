"""Debug script to identify issues with ingest.py"""
import os
import sys
import traceback

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=== Debug Script ===")
print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")

try:
    print("\n1. Testing dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"   API Key loaded: {'Yes' if api_key else 'No'} (len={len(api_key) if api_key else 0})")
    
    print("\n2. Testing langchain imports...")
    from langchain_community.document_loaders import PyPDFLoader
    print("   PyPDFLoader: OK")
    
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("   RecursiveCharacterTextSplitter: OK")
    
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    print("   GoogleGenerativeAIEmbeddings: OK")
    
    from langchain_community.vectorstores import Chroma
    print("   Chroma: OK")
    
    print("\n3. Testing PDF loading...")
    pdf_path = os.path.join(os.path.dirname(__file__), "data", "bitcoin.pdf")
    print(f"   PDF path: {pdf_path}")
    print(f"   PDF exists: {os.path.exists(pdf_path)}")
    
    if os.path.exists(pdf_path):
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        print(f"   Loaded {len(docs)} pages")
        
        print("\n4. Testing text splitting...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        print(f"   Split into {len(chunks)} chunks")
        
        print("\n5. Testing embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Test with a small sample
        test_text = chunks[0].page_content[:100]
        print(f"   Testing embed on: {test_text[:50]}...")
        result = embeddings.embed_query(test_text)
        print(f"   Embedding dimension: {len(result)}")
        
        print("\n6. Creating vector store...")
        db_dir = os.path.join(os.path.dirname(__file__), "src", "chroma_db")
        print(f"   DB directory: {db_dir}")
        
        vectorstore = Chroma.from_documents(
            documents=chunks[:5],  # Test with just 5 chunks first
            embedding=embeddings,
            persist_directory=db_dir
        )
        print("   Vector store created!")
        
        print("\n=== All tests passed! ===")
    else:
        print("   ERROR: PDF file not found!")
        
except Exception as e:
    print(f"\n!!! ERROR !!!")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
