import logging
import numpy as np
import ollama
from typing import List, Optional

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Handles text embedding generation using BGE-M3 via Ollama API"""
    
    def __init__(self, model: str = "bge-m3"):
        self.model = model
        self.embedding_size = 1024  # BGE-M3 embedding size
        
    def generate_embeddings(self, text: str) -> Optional[List[float]]:
        """Generate embeddings for input text"""
        try:
            # Call Ollama API for embeddings
            response = ollama.embeddings(
                model=self.model,
                prompt=text
            )
            
            # Convert to numpy array and validate size
            embeddings = np.array(response['embedding'])
            if len(embeddings) != self.embedding_size:
                logger.error(f"Unexpected embedding size: {len(embeddings)}")
                return None
                
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return None

    def batch_generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for multiple texts"""
        try:
            embeddings = []
            for text in texts:
                emb = self.generate_embeddings(text)
                if emb is None:
                    return None
                embeddings.append(emb)
            return embeddings
        except Exception as e:
            logger.error(f"Error in batch embedding generation: {str(e)}")
            return None
