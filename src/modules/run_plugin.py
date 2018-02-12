# -*- coding:utf-8 -*-
'''
This Class is to load and run plugin
'''

from binding import Binding
from SBase import SBase
from handle_exception import handle_exception

class RunPlugin(SBase):
    '''
    Run Plugin
    '''
    def __init__(self, *args, **kargs):
        '''
        init
        '''

        super(RunPlugin, self).__init__()

        _modules = {
                'convert'           :   'Convert'
                }

        Binding().binding(self, modules = _modules, entity = self)

        self.run_plugin(*args, **kargs)

    def build_type(self, plugin_type, prefix):
        '''
        construct class name from plugin type i.e.
        '''
        _module = self.convert(underscore=(prefix, plugin_type))
        _parts  = [self.convert(upper_first=x) for x in _module.split('_')]
        _class  = self.convert(join=_parts)
        return (_module, _class)

    @handle_exception
    def run_plugin(self, *args, **kargs):
        '''
        Run Plugins
        '''
        if 'plugin' in kargs:
            _type = kargs['plugin']
            _prefix = kargs['prefix'] if 'prefix' in kargs else 'plugin'
            (_module_name, _class_name) = self.build_type(_type, _prefix)
            _cmd = 'from %s import %s' % (_module_name, _class_name)
            exec _cmd in globals()
            _class  = eval(_class_name)
            _plugin = _class()
            return _plugin.run(*args, **kargs)
