import logging
from datetime import datetime

def run():
    """Start the application"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Starting Project Documentation Assistant at {startup_time}")
    logger.info("Application initialized successfully")

if __name__ == "__main__":
    run()
