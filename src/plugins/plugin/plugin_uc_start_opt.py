# -*- coding:utf-8 -*-

from plugin_opt import PluginOpt
from handle_exception import handle_exception

class PluginUcStartOpt(PluginOpt):
    '''
    Plugin for Uc Start Operation
    '''
    _EVENT_LEVELS = 2
    def __init__(self, *args, **kargs):
        '''
        init
        '''
        super(PluginUcStartOpt, self).__init__(*args, **kargs)

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
    def _start(self, *args, **kargs):
        self.load_config()
        self._process_events(self.cm.events)

    @handle_exception
    def process_result(self, result, *args, **kargs):
        '''
        process single event result
        '''
        return super(PluginUcStartOpt, self).main_process_result(result, *args, **kargs)
