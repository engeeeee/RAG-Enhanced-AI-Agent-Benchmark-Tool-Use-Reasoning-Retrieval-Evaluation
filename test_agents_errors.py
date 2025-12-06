"""
Test script to capture errors from agents
"""
import sys
import traceback
import os

# Set up path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

print("=" * 60)
print("Testing Pure Agent")
print("=" * 60)

try:
    from agents.pure_agent import PureAgent
    print("PureAgent import: SUCCESS")
    
    agent = PureAgent()
    print("PureAgent init: SUCCESS")
    
    result = agent.query("What is Bitcoin?")
    print(f"PureAgent query: SUCCESS\n{result[:200]}...")
    
except Exception as e:
    print(f"PureAgent ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing RAG Agent")
print("=" * 60)

try:
    from agents.rag_agent import RAGAgent
    print("RAGAgent import: SUCCESS")
    
    agent = RAGAgent()
    print("RAGAgent init: SUCCESS")
    
    result = agent.query("What is Bitcoin?")
    print(f"RAGAgent query: SUCCESS\n{result[:200]}...")
    
except Exception as e:
    print(f"RAGAgent ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
