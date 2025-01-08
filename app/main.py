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
        for doc in documents:
            logger.info(f"Processed {doc['filename']} ({doc['filetype']})")
            
            # Test embeddings generation
            embedder = EmbeddingGenerator()
            embeddings = embedder.generate_embeddings(doc['content'])
            
            if embeddings:
                logger.info(f"Generated embeddings of size {len(embeddings)} for {doc['filename']}")
            else:
                logger.warning(f"Failed to generate embeddings for {doc['filename']}")
    else:
        logger.warning("No documents found or processed")
    
    logger.info("Application initialized successfully")

if __name__ == "__main__":
    run()
