import os
import sys

print("Python executable:", sys.executable)
print("CWD:", os.getcwd())
print("__file__:", __file__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
print("PROJECT_ROOT:", PROJECT_ROOT)

DB_DIR = os.path.join(PROJECT_ROOT, "chroma_db")
print("DB_DIR:", DB_DIR)
print("DB_DIR exists:", os.path.exists(DB_DIR))

# Simulate rag_agent path logic
agent_path = os.path.join(PROJECT_ROOT, "src", "agents", "rag_agent.py")
print("Agent path:", agent_path)

agent_root = os.path.dirname(os.path.dirname(os.path.dirname(agent_path)))
print("Calculated root from agent path:", agent_root)
