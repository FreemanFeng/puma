# -*- coding:utf-8 -*-
'''
This Class is used to send tcp request
'''
from plugin_opt import PluginOpt
from handle_exception import handle_exception

class PluginIdCache(PluginOpt):
    '''
    Plugin for TCP related operations
    '''
    def __init__(self, *args, **kargs):
        '''
        register callback functions in init stage
        '''
        super(PluginIdCache, self).__init__(*args, **kargs)

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
    def _create_id(self, data, *args, **kargs):
        (imei, mac) = data
        _timestamp = self.convert(now=3)
        _data = self.convert(join=(imei, mac, _timestamp))
        return self.convert(md5=_data)

    @handle_exception
    def process_result(self, result, *args, **kargs):
        '''
        process single event result
        '''
        return super(PluginIdCache, self).main_process_result(result, *args, **kargs)
