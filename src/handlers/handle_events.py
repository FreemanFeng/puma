# -*- coding:utf-8 -*-
'''
This Class is to register plugins
'''
from SBase import SBase
from binding import Binding
from static_mobs import StaticMobs
from handle_exception import handle_exception

class HandleEvents(SBase):
    '''
    HandleEvents class
    '''
    def __init__(self, *args, **kargs):
        '''
        Binding all modules at init stage
        '''
        super(HandleEvents, self).__init__()
        self.event      = None
        _modules = StaticMobs().mobs
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def _set_levels(self, data, *args, **kargs):
        '''
        Use levels to specify levels list for post handling events
        '''
        self.event.result['levels'] = data

    @handle_exception
    def _set_events(self, data, *args, **kargs):
        '''
        Use events config file to be reused
        '''
        if type(data) is not list:
            data = [data]

        self.event.result['events'] = list()

        for _events in data:
            self.cm.load_yaml(_events)
            self.event.result['events'].extend(self.cm.events)

    @handle_exception
    def _set_result(self, name, value):
        self.event.result[name] = value

    @handle_exception
    def _set_config(self, *args, **kargs):
        if self.cm.params:
            for _name, _data in self.cm.params.items():
                self._set_result(_name, _data)

    @handle_exception
    def run(self, *args, **kargs):
        '''
        run handler
        '''
        if 'event' in kargs:
            self.event      = kargs['event']
            _handler        = self.event.handler
            kargs[_handler] = self.event.data
            return self.inner_call(entity=self, *args, **kargs)
