# -*- coding:utf-8 -*-
'''
This Class is base class for plugin
'''
from SBase import SBase
from binding import Binding
from static_mobs import StaticMobs
from handle_exception import handle_exception

class PluginBase(SBase):
    '''
    Plugin Base
    '''
    def __init__(self, *args, **kargs):
        '''
        binding some modules in init stage
        '''
        super(PluginBase, self).__init__()

        self.events = None
        self.params = dict()

        _modules = StaticMobs().mobs
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def handle_events(self, *args, **kargs):
        '''
        should be implemented by child class
        '''
        pass

    @handle_exception
    def loop_events(self, *args, **kargs):
        '''
        should be implemented by child class
        '''
        pass

    @handle_exception
    def main_handle_events(self, level=0, *args, **kargs):
        '''
        handle events
        '''
        self.event_opt(add_events=self.events, params=self.params, level=level)
        self.event_opt(handle_events=self.events, level=level)
        return self.event_opt(results=1)

    @handle_exception
    def main_loop_events(self, *args, **kargs):
        '''
        handle events and reset events for handling again
        '''
        self.main_handle_events(*args, **kargs)
        _results = self.event_opt(results=1)
        self.event_opt(init_events=1)
        return _results

    @handle_exception
    def run(self, *args, **kargs):
        '''
        run plugin
        '''
        result = self.inner_call(entity=self, *args, **kargs)
        self.event_opt(clear_events=1)
        return result
