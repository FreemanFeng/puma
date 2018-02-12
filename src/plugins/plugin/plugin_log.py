# -*- coding:utf-8 -*-
'''
This Class is used to send tcp request
'''
from plugin_opt import PluginOpt
from binding import Binding
from handle_exception import handle_exception

class PluginLog(PluginOpt):
    '''
    Plugin for TCP related operations
    '''
    def __init__(self, *args, **kargs):
        '''
        register callback functions in init stage
        '''
        super(PluginLog, self).__init__(*args, **kargs)
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
    def _decode(self, data, *args, **kargs):
        return self.convert(decb64=data)

    @handle_exception
    def _snapshot(self, data, *args, **kargs):
        (tcid, imei, mac, image) = data
        _id = mac.replace(':', '').replace('-', '')
        _name = self.convert(join=(tcid, '_', _id, '_', imei, '_snapshot.jpg'))
        return self.file_opt(write_binary=(_name, image))

    @handle_exception
    def _join(self, data, *args, **kargs):
        (key1, key2) = data
        return self.convert(join=(key1, '_', key2))

    @handle_exception
    def _cache_status(self, data, *args, **kargs):
        _cache_server   = data['cache_server']
        _id             = data['id']
        _tcid           = data['tcid']
        _mac            = data['mac']
        _type           = data['type']
        _proxy          = data['proxy']
        _config = dict()
        #_path   = self.convert(join=(_proxy['id_cache'], '/cachelog'))
        _path   = '/auto/ucstart/idcache/cachelog'
        _url    = self.convert(join=('http://', _cache_server, _path))
        _params = self.convert(join=('?id=', _id, '&tcid=', _tcid, '&mac=',
                                     _mac, '&type=', _type))
        _config['url'] = self.convert(join=(_url, _params))
        self.get_url(_config)

    @handle_exception
    def process_result(self, result, *args, **kargs):
        '''
        process single event result
        '''
        return super(PluginLog, self).main_process_result(result, *args, **kargs)
