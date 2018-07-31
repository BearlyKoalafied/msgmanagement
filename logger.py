import logging
import util

MSG_LOGGER = "msglogger"

def prep(logger_name):
    logger = logging.getLogger(logger_name)
    fh = logging.FileHandler(util.relative_file_path(__file__, 'redditmsg.log'))
    fmt = logging.Formatter('[%(levelname)s] [%(asctime)s]: %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)

def get_logger(logger_name):
    return logging.getLogger(logger_name)
