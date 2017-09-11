#-*-coding:utf8-*-
import logging
from application import app

log_path = app.config.get('LOG')
log_level = app.config.get('LOG_LEVEL')
logger = logging.getlogger('bindlog')
fmter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
handler = logging.FileHandler(log_path)
handler.setFormatter(fmt=fmter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
