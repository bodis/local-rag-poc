import re
import logging
from typing import List, Optional
from urllib.parse import urlparse
from pathlib import Path

logger = logging.getLogger(__name__)

class URLIngestor:
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
    
    def read_url_file(self, file_path: Path) -> List[str]:
        """
        Read a .url file and extract valid URLs
        
        Args:
            file_path: Path to the .url file
            
        Returns:
            List of valid URLs found in the file
        """
        if not file_path.exists() or file_path.suffix.lower() != '.url':
            logger.warning(f"Invalid file path or extension: {file_path}")
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = []
                for line in f:
                    line = line.strip()
                    if self.is_valid_url(line):
                        urls.append(line)
                        logger.debug(f"Found valid URL: {line}")
                    else:
                        logger.debug(f"Skipping invalid URL: {line}")
                return urls
        except Exception as e:
            logger.error(f"Error reading URL file {file_path}: {str(e)}")
            return []
