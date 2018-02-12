# -*- coding: utf-8 -*-
'''
This is the Base library for multi-instanced class
'''
import sys
from binding import Binding
from logger import Logger
from static_mobs import StaticMobs
from config_manager import ConfigManager

class MBase(object):
    '''
    Base library
    '''
    def __init__(self, *args, **kargs):
        #reload(sys)
        #sys.setdefaultencoding('utf-8')
        _modules = StaticMobs().mobs
        Binding().binding(self, modules = _modules, entity = self)
        self.root_path  = self.get_root_path()
        self.add_path(self.absolute_path('src'))

    @property
    def cm(self):
        return ConfigManager()

    @property
    def logger(self):
        if self.cm.mode == 'robot':
            return Logger().get_robot_logger()
        return Logger().get_logger()

    def _get(self, key, *args, **kargs):
        return getattr(self, key)

    def _set(self, data, *args, **kargs):
        (key, value) = data
        return setattr(self, key, value)

    def load_extra_config(self, config, *args, **kargs):
        '''
        load extra config files
        '''
        self.cm.load_yaml(self.absolute_path(config))
        if self.cm.configs and type(self.cm.configs) is list:
            [self.cm.load_yaml(self.absolute_path(x)) for x in self.cm.configs]

    def load_config(self, *args, **kargs):
        '''
        load extra config files
        '''
        if self.cm.mode is None:
            _config = sys.argv[1]
            self.load_extra_config(_config)
