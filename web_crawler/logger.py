# -*- coding: utf8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class _Logger(object):
    def __init__(self, log_project='script', log_filename='consumer.log', log_dir='/app/log/script', log_handler='day'):
        self.log_project = log_project
        self.log_filename = log_filename
        self.log_dir = log_dir
        self.log_handler = log_handler

    def set_log_file(self, log_project, log_filename, log_dir, log_handler):
        """
        设置日志文件,加载不同的配置
        :param log_project:
        :param log_filename:
        :param log_dir:
        :param log_handler:
        :return:
        """
        self.log_project = log_project
        self.log_filename = log_filename
        self.log_dir = log_dir
        self.log_handler = log_handler

    def getLogger(self):
        if os.path.isdir(self.log_dir):
            log_dir = os.path.join(self.log_dir, self.log_project)
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            log_file = os.path.join(log_dir, self.log_filename)
        else:
            log_file = os.path.join(os.path.dirname(__file__), self.log_filename)

        LOGGER = logging.getLogger(__name__)
        handler = None
        if self.log_handler == 'day':
            handler = TimedRotatingFileHandler(log_file, when='midnight')
        elif self.log_handler == 'rotate':
            handler = RotatingFileHandler(log_file, mode='a', maxBytes=100 * 1024 * 1024, backupCount=10)
        simple_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        handler.setFormatter(simple_formatter)
        LOGGER.addHandler(handler)
        LOGGER.setLevel(logging.INFO)
        logging.getLogger('requests').setLevel(logging.WARNING)
        return LOGGER
