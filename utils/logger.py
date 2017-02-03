# -*- coding: utf-8 -*-
import logging
import sys

from .color_formatter import ColoredFormatter

# add level 'success'
logging.SUCCESS = 25  # 25 is between WARNING(30) and INFO(20)
logging.addLevelName(logging.SUCCESS, 'SUCCESS')


def getLogger(logger_name, logger_level=logging.INFO):
    try:
        logger = logging.getLogger(logger_name)
    except Exception:
        logger = logging.getLogger(__name__)

    logger.setLevel(logger_level)
    logger.success = lambda msg, *args, **kwargs: logger.log(logging.SUCCESS, msg, *args, **kwargs)
    handler = logging.StreamHandler(sys.stdout)  # thread.lock
    # handler = logging.FileHandler('{}/doge_{}.log'.format(Logger.LOGGER_PATH, logger_name))
    formatter = ColoredFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = getLogger('tools')
