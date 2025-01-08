import requests
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LocalLLM:
    """Handles communication with local LLM API"""
    
    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url
        self.chat_endpoint = f"{self.base_url}/v1/chat/completions"
        
    def generate_response(self, context: str, question: str) -> Optional[str]:
        """
        Generate a response from the LLM using provided context and question
        
        Args:
            context: Relevant context from vector store
            question: Original user question
            
        Returns:
            Generated response text or None if error occurs
        """
        try:
            # Construct the prompt with context and question
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Use the provided context to answer the question."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
            
            # Prepare the request payload
            payload = {
                "model": "local-model",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(
                self.chat_endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            
            # Check for successful response
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"LLM API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return None
            
    def test_connection(self) -> bool:
        """Test if the LLM API is reachable"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
