import re
import logging
import requests
from typing import List, Optional, Tuple
from urllib.parse import urlparse
from pathlib import Path
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class URLIngestor:
    """Handles ingestion of URLs and their web content"""
    """Handles ingestion of URLs from .url files"""
    
    def __init__(self):
        self.url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    def is_valid_url(self, url: str) -> bool:
        """Validate if a string is a properly formatted URL"""
        if not url or not isinstance(url, str):
            return False
        return bool(self.url_pattern.match(url.strip()))
    
    def fetch_web_content(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Fetch and clean web page content
        
        Args:
            url: URL to fetch content from
            
        Returns:
            Tuple of (cleaned text content, page title) or None if error occurs
        """
        try:
            # Fetch the page content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
                element.decompose()
                
            # Get page title
            title = soup.title.string.strip() if soup.title else url
            
            # Clean and extract text
            text = soup.get_text(separator='\n')
            cleaned_text = '\n'.join(
                line.strip() for line in text.splitlines() 
                if line.strip()
            )
            
            logger.debug(f"Successfully fetched content from {url}")
            return cleaned_text, title
            
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {str(e)}")
            return None

    def read_url_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """
        Read a .url file and extract valid URLs with their content
        
        Args:
            file_path: Path to the .url file
            
        Returns:
            List of tuples containing (URL, cleaned content) for each valid URL
        """
        if not file_path.exists() or file_path.suffix.lower() != '.url':
            logger.warning(f"Invalid file path or extension: {file_path}")
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                results = []
                for line in f:
                    line = line.strip()
                    if self.is_valid_url(line):
                        content = self.fetch_web_content(line)
                        if content:
                            results.append((line, content[0]))
                            logger.debug(f"Processed URL: {line}")
                    else:
                        logger.debug(f"Skipping invalid URL: {line}")
                return results
        except Exception as e:
            logger.error(f"Error reading URL file {file_path}: {str(e)}")
            return []
