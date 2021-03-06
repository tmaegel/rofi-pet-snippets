# coding=utf-8
import logging
import logging.handlers
import os

logger = logging.getLogger(os.path.basename(__name__))
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address="/dev/log")
logger.addHandler(handler)
handler.setFormatter(logging.Formatter("%(name)10s - %(levelname)8s - %(message)s"))
