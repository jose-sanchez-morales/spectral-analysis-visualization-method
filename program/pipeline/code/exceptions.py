import logging
from logging import handlers


def get_module_logger(module_name):

    logger = logging.getLogger(module_name)
    programlogger = logging.handlers.RotatingFileHandler('pipeline.log', maxBytes=100000, backupCount=1)
    programlogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    programlogger.setFormatter(formatter)
    logger.addHandler(programlogger)
    return logger
