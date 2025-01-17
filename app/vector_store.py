import numpy as np
from typing import List, Dict, Optional
import logging
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class VectorStore:
    """In-memory vector store for document embeddings with metadata"""
    
    def __init__(self):
        self.embeddings = []
        self.metadata = []
        
    def add_document(self, embedding: List[float], metadata: Dict) -> None:
        """
        Add a document embedding with associated metadata to the store
        
        Args:
            embedding: List of floats representing the document embedding
            metadata: Dictionary containing document metadata (filename, content snippet, etc.)
        """
        if not embedding or not metadata:
            logger.warning("Cannot add empty embedding or metadata")
            return
            
        self.embeddings.append(np.array(embedding))
        self.metadata.append(metadata)
        logger.info(f"Added document {metadata.get('filename', 'unknown')} to vector store")
        
    def search(self, query_embedding: List[float], top_k: int = 3, min_similarity: float = 0.7) -> List[Dict]:
        """
        Search for similar documents using cosine similarity
        
        Args:
            query_embedding: Embedding vector for the search query
            top_k: Number of top results to return
            min_similarity: Minimum similarity score to consider a result relevant
            
        Returns:
            List of dictionaries containing metadata and similarity score for top matches
            that meet the minimum similarity threshold
        """
        if not self.embeddings:
            logger.warning("No documents in vector store to search")
            return []
            
        # Convert query embedding to numpy array
        query_vec = np.array(query_embedding).reshape(1, -1)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(
            query_vec,
            np.array(self.embeddings)
        )[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            similarity_score = float(similarities[idx])
            logger.debug(f"Found result with similarity score: {similarity_score:.4f}")
            
            if similarity_score >= min_similarity:
                result = self.metadata[idx].copy()
                result['similarity'] = similarity_score
                results.append(result)
            else:
                logger.debug(f"Skipping result with low similarity: {similarity_score:.4f}")
                
        return results
        
    def clear(self) -> None:
        """Clear all stored embeddings and metadata"""
        self.embeddings = []
        self.metadata = []
        logger.info("Cleared vector store")
        
    def size(self) -> int:
        """Return number of documents in the store"""
        return len(self.embeddings)
