# -*- coding:utf-8 -*-
'''
This Class is to get basic config
'''
import yaml
import os
import os.path
from paths import Paths
from singleton import Singleton
from handle_exception import handle_exception

class ConfigManager(Singleton):
    '''
    Singleton class for Config Manager
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(ConfigManager, self).__init__()

        self.config_file = kargs.get('config_file', "etc/startup.yml")

        self.config = dict()
        self.init_config()

    @handle_exception
    def load_yaml(self, config_file, entity = None):
        '''
        load config from yaml file and generate a dict object
        '''
        #print 'Load yaml file %s' % config_file
        _path_obj   = Paths()
        _config     = _path_obj.absolute_path(config_file)
        test_config = yaml.load(file(_config))
        self.load_dict(test_config, entity)

    @handle_exception
    def _set_value(self, entity, key, value):
        _attr = getattr(entity, key, None)
        if _attr is None:
            entity.__setattr__(key, value)
        elif type(_attr) is dict and type(value) is dict:
            _attr.update(value)
        else:
            entity.__setattr__(key, value)

    @handle_exception
    def load_dict(self, data, entity=None):
        '''
        set attrbutes for keys in dict object
        '''
        for key, value in data.items():
            if key == 'load_config':
                self.load_yaml(value, entity)
            elif entity == None:
                self._set_value(self, key, value)
                self.config[key] = value
            else:
                self._set_value(entity, key, value)

    @handle_exception
    def update_attr(self, data, attr):
        '''
        update attr
        '''
        if type(attr) is not dict:
            return

        for key, value in data.items():
            if key in attr and type(attr[key]) is dict and type(value) is dict:
                self.update_attr(value, attr[key])
            else:
                attr[key] = value

    @handle_exception
    def update_dict(self, data, entity=None):
        '''
        update attrbutes for keys in dict object
        '''
        if not entity:
            entity = self

        for key, value in data.items():
            _attr = getattr(entity, key)
            if _attr and type(_attr) is dict and type(value) is dict:
                self.update_attr(value, _attr)
                entity.__setattr__(key, _attr)
            else:
                return self.load_dict(data, entity)

    @handle_exception
    def reset_config(self):
        '''
        reset config to init stage
        '''
        self.clear_config()
        self.init_config()

    @handle_exception
    def clear_config(self):
        '''
        clear the config
        '''
        for key in self.config.keys():
            self.__delattr__(key)
        self.config.clear()

    @handle_exception
    def init_config(self):
        '''
        init the config
        '''
        self.load_yaml(self.config_file)

    def get_config(self):
        return self.config

    def show_config(self):
        print self.config
