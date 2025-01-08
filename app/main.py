import logging
from datetime import datetime
from document_ingestion import DocumentIngestor
from embeddings import EmbeddingGenerator

def run():
    """Start the application"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Starting Project Documentation Assistant at {startup_time}")
    
    # Test document ingestion
    ingestor = DocumentIngestor()
    documents = ingestor.ingest_documents()
    
    if documents:
        logger.info(f"Successfully ingested {len(documents)} documents")
        
        # Initialize vector store
        from vector_store import VectorStore
        vector_store = VectorStore()
        
        # Process and store documents
        embedder = EmbeddingGenerator()
        for doc in documents:
            logger.info(f"Processing {doc['filename']} ({doc['filetype']})")
            
            # Generate embeddings
            embeddings = embedder.generate_embeddings(doc['content'])
            
            if embeddings:
                # Store document with metadata
                metadata = {
                    'filename': doc['filename'],
                    'filetype': doc['filetype'],
                    'content_snippet': doc['content'][:200] + "..."  # Store first 200 chars
                }
                vector_store.add_document(embeddings, metadata)
                logger.info(f"Stored {doc['filename']} in vector store")
            else:
                logger.warning(f"Failed to generate embeddings for {doc['filename']}")
        
        # Test search and LLM integration
        if vector_store.size() > 0:
            test_query = "project documentation"  # Example search term
            query_embedding = embedder.generate_embeddings(test_query)
            if query_embedding:
                results = vector_store.search(query_embedding, min_similarity=0.7)
                logger.info(f"Search results for '{test_query}':")
            
                # Get top result's content snippet if we have relevant results
                if results:
                    top_result = results[0]
                    context = top_result['content_snippet']
                    logger.info(f"Using top result with similarity: {top_result['similarity']:.4f}")
                else:
                    # No relevant results found
                    logger.info("No relevant results found in vector store")
                    response = "I'm sorry, but I don't have any relevant information about that topic in my active memory."
                    logger.info(f"LLM response:\n{response}")
                    return
                    
                    # Initialize LLM
                    from local_llm import LocalLLM
                    llm = LocalLLM()
                    
                    # Test LLM connection
                    if llm.test_connection():
                        logger.info("LLM connection successful")
                        
                        # Generate response using context
                        response = llm.generate_response(
                            context=context,
                            question=test_query
                        )
                        
                        if response:
                            logger.info(f"LLM response:\n{response}")
                        else:
                            logger.warning("Failed to generate LLM response")
                    else:
                        logger.error("Could not connect to LLM API")
    else:
        logger.warning("No documents found or processed")
    
    logger.info("Application initialized successfully")

if __name__ == "__main__":
    run()
