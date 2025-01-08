import os
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
import logging

logger = logging.getLogger(__name__)

class DocumentIngestor:
    """Handles ingestion of documents from input directory"""
    
    def __init__(self, input_dir: str = "input"):
        self.input_dir = Path(input_dir)
        if not self.input_dir.exists():
            logger.warning(f"Input directory {self.input_dir} does not exist")
            self.input_dir.mkdir(parents=True, exist_ok=True)

    def get_supported_extensions(self) -> List[str]:
        """Return list of supported file extensions"""
        return [".pdf", ".md", ".url"]

    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if file has supported extension"""
        return file_path.suffix.lower() in self.get_supported_extensions()

    def _read_pdf(self, file_path: Path) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() for page in reader.pages)
                return text
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {str(e)}")
            return None

    def _read_markdown(self, file_path: Path) -> Optional[str]:
        """Read markdown file content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading Markdown {file_path}: {str(e)}")
            return None
            
    def _read_url_file(self, file_path: Path) -> Optional[str]:
        """Read URL file and return concatenated web content"""
        from url_ingestion import URLIngestor
        url_ingestor = URLIngestor()
        url_contents = url_ingestor.read_url_file(file_path)
        if not url_contents:
            return None
            
        # Combine all web content with source URLs as headers
        combined = []
        for url, content in url_contents:
            combined.append(f"=== Content from {url} ===\n{content}\n")
        return "\n".join(combined) if combined else None

    def ingest_documents(self) -> List[Dict[str, str]]:
        """Ingest all supported documents from input directory"""
        documents = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and self._is_supported_file(file_path):
                logger.info(f"Processing file: {file_path.name}")
                
                content = None
                if file_path.suffix.lower() == ".pdf":
                    content = self._read_pdf(file_path)
                elif file_path.suffix.lower() == ".md":
                    content = self._read_markdown(file_path)
                elif file_path.suffix.lower() == ".url":
                    content = self._read_url_file(file_path)
                
                if content:
                    documents.append({
                        "filename": file_path.name,
                        "content": content,
                        "filetype": file_path.suffix.lower()
                    })
        
        return documents
