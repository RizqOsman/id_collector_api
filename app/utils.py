import logging
from fastapi import Depends
from .database import SessionLocal
import os
import sys
from datetime import datetime

def get_db():
    """
    Dependency function to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def setup_logger():
    """
    Set up and configure logger
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Get current timestamp for log file name
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = f"logs/api_{timestamp}.log"
    
    # Configure logger
    logger = logging.getLogger("id_collector_api")
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
