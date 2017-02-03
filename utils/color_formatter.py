# -*- coding: utf-8 -*-

import datetime
import logging

from color import colored


class ColoredFormatter(logging.Formatter):
    """this is colored formatter"""

    def format(self, record):
        message = record.getMessage()
        mapping = {
            'CRITICAL': 'bgred',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'SUCCESS': 'green',
            'INFO': 'cyan',
            'DEBUG': 'bggrey',
        }

        # default color
        color = mapping.get(record.levelname, "write")
        level = colored('%-8s' % record.levelname, color)
        time = colored(datetime.datetime.now().strftime("(%H:%M:%S)"), "magenta")
        return " ".join([level, time, message])
