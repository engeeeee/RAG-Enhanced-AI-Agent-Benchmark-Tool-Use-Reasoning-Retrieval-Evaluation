"""
Test RAG Agent and capture detailed errors
"""
import traceback
import sys
import os

# Redirect output
log_file = open("test_rag_output.txt", "w", encoding="utf-8", buffering=1)
sys.stdout = log_file
sys.stderr = log_file

try:
    print("Step 1: Importing dependencies...")
    import os
    from dotenv import load_dotenv
    print("  - dotenv loaded")
    
    import google.generativeai as genai
    print("  - google.generativeai loaded")
    
    from langchain_community.vectorstores import Chroma
    print("  - Chroma loaded")
    
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("  - HuggingFaceEmbeddings loaded")
    
    print("\nStep 2: Loading environment variables...")
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    print("  - API Key loaded: " + ("Yes" if api_key else "No"))
    
    print("\nStep 3: Configuring Gemini...")
    genai.configure(api_key=api_key)
    print("  - Gemini configured")
    
    print("\nStep 4: Checking chroma_db path...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(project_root, "chroma_db")
    print("  - DB path: " + db_dir)
    print("  - Exists: " + str(os.path.exists(db_dir)))
    
    print("\nStep 5: Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    print("  - Embeddings loaded")
    
    print("\nStep 6: Loading Chroma vectorstore...")
    vectorstore = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )
    print("  - Vectorstore loaded")
    print("  - Collection count: " + str(vectorstore._collection.count()))
    
    print("\nStep 7: Creating Gemini model...")
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("  - Model created")
    
    print("\nStep 8: Test retrieval...")
    docs = vectorstore.similarity_search("bitcoin", k=2)
    print("  - Retrieved " + str(len(docs)) + " documents")
    
    print("\nStep 9: Test generation...")
    response = model.generate_content("Say hello")
    print("  - Response: " + response.text)
    
    print("\nAll tests passed!")

except Exception as e:
    print("\nError occurred: " + str(type(e).__name__) + ": " + str(e))
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
