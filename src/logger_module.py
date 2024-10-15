import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', level=logging.INFO, max_bytes=5 * 1024 * 1024, backup_count=5, logger_name='logger_module'):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    
    
    console_handler = logging.StreamHandler()
    
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    
    logger = logging.getLogger(logger_name) 
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_message(level, message, logger_name='logger_module'):
    logger = logging.getLogger(logger_name)
    
    
    level_dict = {
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'debug': logger.debug
    }
    
    log_function = level_dict.get(level, logger.debug)
    log_function(message)