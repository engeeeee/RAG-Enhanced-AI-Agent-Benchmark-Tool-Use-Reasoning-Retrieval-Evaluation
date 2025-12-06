"""
Debug RAG Agent errors - Minimal
"""
import sys
import os
import traceback

log_path = "debug_log_minimal.txt"

try:
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("Starting debug...\n")
    
    # Add src to path
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"Project root: {PROJECT_ROOT}\n")
        f.write("Importing RAGAgent...\n")

    from agents.rag_agent import RAGAgent
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("RAGAgent imported successfully.\n")
        f.write("Creating agent...\n")
        
    agent = RAGAgent()
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("Agent created successfully.\n")

except Exception as e:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\nERROR: {type(e).__name__}: {e}\n")
        f.write(traceback.format_exc())
    sys.exit(1)
