"""
Pure Agent - Relies entirely on model's own knowledge + reasoning chain
Does not use any external knowledge base
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key validation
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not found. Please check your .env file")

genai.configure(api_key=api_key)


class PureAgent:
    """
    Pure Agent: Only relies on Gemini model's pre-trained knowledge to answer questions
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize the Pure Agent with Gemini model"""
        try:
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {e}")
            
        self.system_prompt = """You are an expert in cryptocurrency and blockchain technology.
Please answer the following questions based on your knowledge.
Requirements:
1. Be accurate and specific
2. Explain technical details thoroughly when applicable
3. Clearly state if you are uncertain
"""
    
    def query(self, question: str) -> str:
        """Query the model and return the answer"""
        full_prompt = f"{self.system_prompt}\n\nQuestion: {question}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "PermissionDenied" in error_msg:
                return f"Error: API key issue - {error_msg}. Please check your GOOGLE_API_KEY in .env file."
            return f"Error generating response: {error_msg}"
    
    def query_with_reasoning(self, question: str) -> dict:
        """Query with reasoning chain, returns detailed reasoning process"""
        reasoning_prompt = f"""{self.system_prompt}

Please answer the question following these steps:
1. First analyze the key points of the question
2. List relevant facts you know
3. Perform logical reasoning
4. Provide the final answer

Question: {question}

Please respond in the following format:
## Question Analysis
[Your analysis]

## Relevant Knowledge
[Facts you know]

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
            "full_response": full_response,
            "agent_type": "pure_agent"
        }


if __name__ == "__main__":
    # Test Pure Agent
    agent = PureAgent()
    
    test_questions = [
        "What is Bitcoin's consensus mechanism?",
        "Explain the double-spending problem in the Bitcoin whitepaper",
    ]
    
    for q in test_questions:
        print(f"\n{'='*50}")
        print(f"Question: {q}")
        result = agent.query_with_reasoning(q)
        print(result["full_response"])
