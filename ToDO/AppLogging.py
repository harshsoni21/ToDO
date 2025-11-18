import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent
app_log_dir = os.path.join(BASE_DIR, 'logs')

os.makedirs(app_log_dir, exist_ok=True)


def init_app_logger(logger_name):
    c_formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s', datefmt='%d-%m-%y,%I:%M:%S%p')
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    debug_fh = RotatingFileHandler(app_log_dir + f'/{logger_name}_Debug.log', maxBytes=5 * 1024 * 1024, backupCount=2)
    debug_fh.setLevel(logging.DEBUG)
    debug_fh.setFormatter(c_formatter)
    logger.addHandler(debug_fh)
    
    info_fh = RotatingFileHandler(app_log_dir + f'/{logger_name}_Info.log', maxBytes=5 * 1024 * 1024, backupCount=2)
    info_fh.setLevel(logging.INFO)
    info_fh.setFormatter(c_formatter)
    logger.addHandler(info_fh)
    
    error_fh = RotatingFileHandler(app_log_dir + f'/{logger_name}_Error.log', maxBytes=5 * 1024 * 1024, backupCount=2)
    error_fh.setLevel(logging.ERROR)
    error_fh.setFormatter(c_formatter)
    logger.addHandler(error_fh)
    
    return logger


app_logger = init_app_logger('todo_server_logger')


def update_log_level(level):
    logger_level = logging.ERROR
    if level == 'DEBUG':
        logger_level = logging.DEBUG
    elif level == 'INFO':
        logger_level = logging.INFO
    app_logger.setLevel(logger_level)


def get_logger():
    return app_logger