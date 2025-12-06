import sys
import os

# Write to file directly  
with open(r"d:\download\crypto_rag_experiment\debug_output.txt", "w", encoding="utf-8") as f:
    f.write("=== Python Debug Log ===\n")
    f.write(f"Python version: {sys.version}\n")
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"Script path: {__file__}\n")
    f.write("\n=== Testing imports ===\n")
    
    try:
        from dotenv import load_dotenv
        f.write("dotenv: OK\n")
    except Exception as e:
        f.write(f"dotenv: FAILED - {e}\n")
    
    try:
        import google.generativeai as genai
        f.write("google.generativeai: OK\n")
    except Exception as e:
        f.write(f"google.generativeai: FAILED - {e}\n")
    
    try:
        from langchain_community.vectorstores import Chroma
        f.write("Chroma: OK\n")
    except Exception as e:
        f.write(f"Chroma: FAILED - {e}\n")
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        f.write("HuggingFaceEmbeddings: OK\n")
    except Exception as e:
        f.write(f"HuggingFaceEmbeddings: FAILED - {e}\n")
    
    f.write("\n=== Environment ===\n")
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    f.write(f"API Key present: {bool(api_key)}\n")
    
    f.write("\n=== Chroma DB ===\n")
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
    f.write(f"DB path: {db_dir}\n")
    f.write(f"DB exists: {os.path.exists(db_dir)}\n")
    
    if os.path.exists(db_dir):
        f.write(f"DB contents: {os.listdir(db_dir)}\n")
    
    f.write("\nDone!\n")

print("Test completed - check debug_output.txt")
