# -*- coding:utf-8 -*-
'''
This Class is used to send tcp request
'''
import json

from plugin_opt import PluginOpt
from binding import Binding
from handle_exception import handle_exception

class PluginIdm(PluginOpt):
    '''
    Plugin for TCP related operations
    '''
    def __init__(self, *args, **kargs):
        '''
        register callback functions in init stage
        '''
        super(PluginIdm, self).__init__(*args, **kargs)
        _modules = {
                'http_opt'  :   'HttpOpt'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def do(self, *args, **kargs):
        '''
        interface for plugin operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _join(self, data, *args, **kargs):
        (key1, key2) = data
        return self.convert(join=(key1, '_', key2))

    @handle_exception
    def process_result(self, result, *args, **kargs):
        '''
        process single event result
        '''
        return super(PluginIdm, self).main_process_result(result, *args, **kargs)
