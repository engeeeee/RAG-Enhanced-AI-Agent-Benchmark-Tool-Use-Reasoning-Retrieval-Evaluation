"""
RAG Agent - Combines vector retrieval with Gemini model generation
Uses local HuggingFace embeddings and Chroma vector database
"""
import os
import google.generativeai as genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path configuration - use abspath to ensure correct paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(PROJECT_ROOT, "chroma_db")

# API Key validation
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not found. Please check your .env file")

genai.configure(api_key=api_key)


class RAGAgent:
    """
    RAG Agent: Combines vector retrieval + Gemini model for answer generation
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize the RAG Agent with Gemini model and vector store"""
        try:
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {e}")
        
        # Use local HuggingFace embeddings (same model as ingest)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Load vector database
        if os.path.exists(DB_DIR):
            self.vectorstore = Chroma(
                persist_directory=DB_DIR,
                embedding_function=self.embeddings
            )
        else:
            self.vectorstore = None
            print(f"Warning: Vector database not found at {DB_DIR}. Please run ingest.py first.")
        
        self.system_prompt = """You are an expert in cryptocurrency and blockchain technology.
Please answer questions based on the provided reference materials.
Requirements:
1. Prioritize information from the reference materials
2. Accurately cite source content when applicable
3. If reference materials are insufficient, supplement with your knowledge
4. Clearly distinguish between information from references and your inferences
"""
    
    def retrieve(self, query: str, k: int = 4) -> list:
        """Retrieve relevant documents from vector database"""
        if self.vectorstore is None:
            return []
        
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs
    
    def query(self, question: str) -> str:
        """RAG query: retrieve + generate"""
        # 1. Retrieve relevant documents
        retrieved_docs = self.retrieve(question)
        
        # 2. Build context
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
            for doc in retrieved_docs
        ])
        
        # 3. Build prompt
        full_prompt = f"""{self.system_prompt}

## Reference Materials
{context if context else "No reference materials available"}

## Question
{question}

Please answer based on the above reference materials:"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "PermissionDenied" in error_msg:
                return f"Error: API key issue - {error_msg}. Please check your GOOGLE_API_KEY in .env file."
            return f"Error generating response: {error_msg}"
    
    def query_with_reasoning(self, question: str) -> dict:
        """RAG query with reasoning chain, returns detailed information"""
        # 1. Retrieve
        retrieved_docs = self.retrieve(question)
        
        # 2. Build context
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
            for doc in retrieved_docs
        ])
        
        # 3. Prompt with reasoning
        reasoning_prompt = f"""{self.system_prompt}

## Reference Materials
{context if context else "No reference materials available"}

Please answer the question following these steps:
1. First analyze the key points of the question
2. Extract relevant information from reference materials
3. Perform logical reasoning
4. Provide the final answer

Question: {question}

Please respond in the following format:
## Question Analysis
[Your analysis]

## Information from References
[Cited content]

## Reasoning Process
[Your reasoning]

## Final Answer
[Your answer]
"""
        # Safety settings to reduce blocking
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        full_response = ""
        try:
            response = self.model.generate_content(reasoning_prompt, safety_settings=safety_settings)
            full_response = response.text
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "PermissionDenied" in error_msg:
                full_response = f"Error: API key issue - {error_msg}. Please update your GOOGLE_API_KEY."
            else:
                full_response = f"Error: Unable to generate response - {error_msg}"

        return {
            "question": question,
            "retrieved_docs": [
                {
                    "content": doc.page_content[:500],
                    "source": doc.metadata.get("source", "unknown")
                } for doc in retrieved_docs
            ],
            "full_response": full_response,
            "agent_type": "rag_agent"
        }


if __name__ == "__main__":
    # Test RAG Agent
    agent = RAGAgent()
    
    test_questions = [
        "What is Bitcoin's consensus mechanism?",
    ]
    
    for q in test_questions:
        print(f"\n{'='*50}")
        print(f"Question: {q}")
        result = agent.query_with_reasoning(q)
        print(f"\nRetrieved {len(result['retrieved_docs'])} relevant document chunks")
        print(result["full_response"])
