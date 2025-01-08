from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime
from document_ingestion import DocumentIngestor
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from local_llm import LocalLLM

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize components
ingestor = DocumentIngestor()
embedder = EmbeddingGenerator()
vector_store = VectorStore()
llm = LocalLLM()

def initialize_application():
    """Initialize the application components"""
    logging.basicConfig(level=logging.INFO)
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Starting Project Documentation Assistant at {startup_time}")
    
    # Ingest documents
    documents = ingestor.ingest_documents()
    
    if documents:
        logger.info(f"Successfully ingested {len(documents)} documents")
        for doc in documents:
            logger.info(f"Processing {doc['filename']} ({doc['filetype']})")
            embeddings = embedder.generate_embeddings(doc['content'])
            
            if embeddings:
                metadata = {
                    'filename': doc['filename'],
                    'filetype': doc['filetype'],
                    'content_snippet': doc['content'][:200] + "..."
                }
                vector_store.add_document(embeddings, metadata)
                logger.info(f"Stored {doc['filename']} in vector store")
            else:
                logger.warning(f"Failed to generate embeddings for {doc['filename']}")
    else:
        logger.warning("No documents found or processed")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle user questions"""
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Please provide a question'}), 400
    
    logger.info(f"Processing question: {question}")
    
    # Generate embedding for the question
    query_embedding = embedder.generate_embeddings(question)
    if not query_embedding:
        return jsonify({'error': 'Failed to process question'}), 500
    
    # Search vector store
    results = vector_store.search(query_embedding, min_similarity=0.2)
    
    if not results:
        return jsonify({
            'response': "I'm sorry, but I don't have any relevant information about that topic in my active memory."
        })
    
    # Use top result as context
    top_result = results[0]
    context = top_result['content_snippet']
    logger.info(f"Using context from: {top_result['filename']}")
    
    # Generate LLM response
    if not llm.test_connection():
        return jsonify({'error': 'LLM service unavailable'}), 503
        
    response = llm.generate_response(context=context, question=question)
    if not response:
        return jsonify({'error': 'Failed to generate response'}), 500
    
    return jsonify({
        'response': response,
        'source': top_result['filename']
    })

def run():
    """Start the application"""
    initialize_application()
    app.run(host='0.0.0.0', port=5123, debug=True)

if __name__ == "__main__":
    run()
