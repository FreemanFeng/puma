# -*- coding:utf-8 -*-
'''
This Class is to set logger formats
'''

import os
import logging
from datetime import datetime

from config_manager import ConfigManager
from binding import Binding
from singleton import Singleton
from handle_exception import handle_exception

class Logger(Singleton):
    '''
    Singleton class for logger
    '''
    def __init__(self, *args, **kargs):
        '''
        init
        '''
        self._logger= None
        self.cm     = ConfigManager()
        self.config = kargs.get('config', self.cm.logger)

        _modules = {
                'paths'             :   'Paths'
                }

        Binding().binding(self, modules = _modules, entity = self)

    def set_console_logger(self, config):
        '''
        set console logger
        '''
        _console = logging.StreamHandler()
        _console.setLevel(level = eval('.'.join(['logging', config['level']])))
        _formatter = logging.Formatter(config['format'])
        _console.setFormatter(_formatter)
        return _console

    def set_file_logger(self, config):
        '''
        set file logger
        '''
        _path = self.absolute_path(self.cm.tmp)
        logging.basicConfig(
                level   = eval('.'.join(['logging', config['level']])),
                format  = config['format'],
                filename= os.path.join(_path, config['filename']),
                datefmt = config['datefmt'],
                filemode= 'w')

    def get_logger(self):
        '''
        config logger
        '''
        if self._logger:
            return self._logger
        self.set_file_logger(self.config['file'])
        self._logger = logging.getLogger(self.config['name'])
        if not self._logger.handlers:
            _handler = self.set_console_logger(self.config['console'])
            self._logger.addHandler(_handler)
        return self._logger

    def info(self, message):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        print _timestamp, message

    def debug(self, message):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        print _timestamp, message

    def error(self, message):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        print _timestamp, message

    def get_robot_logger(self):
        '''
        config logger
        '''
        return self
