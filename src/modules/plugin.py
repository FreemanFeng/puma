# -*- coding:utf-8 -*-
'''
This Class is to register plugins
'''
from SBase import SBase
from binding import Binding
from handle_exception import handle_exception

class Plugin(SBase):
    '''
    Plugin Attributes
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize plugin instance
        '''
        super(Plugin, self).__init__()

        _modules = {
                'run_plugin'    :   'RunPlugin'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def add_plugins(self, plugins, *args, **kargs):
        '''
        binding modules class methods
        '''
        for _plugin in plugins:
            (_module_name, _class_name) = self.build_type(_plugin, 'plugin')
            #print "MODULE %s CLASS %s" % (_module_name, _class_name)
            _cmd = 'from %s import %s' %(_module_name, _class_name)
            exec _cmd in globals()
            _class = eval(_class_name)()
            self.__setattr__(_plugin, _class)
