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
        
        # Test search functionality
        if vector_store.size() > 0:
            test_query = "project documentation"  # Example search term
            query_embedding = embedder.generate_embeddings(test_query)
            if query_embedding:
                results = vector_store.search(query_embedding)
                logger.info(f"Search results for '{test_query}':")
                for result in results:
                    logger.info(f"- {result['filename']} (similarity: {result['similarity']:.3f})")
    else:
        logger.warning("No documents found or processed")
    
    logger.info("Application initialized successfully")

if __name__ == "__main__":
    run()
