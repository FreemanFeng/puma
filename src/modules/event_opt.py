# -*- coding:utf-8 -*-
'''
This Class is to loop events and handle them
'''
from SBase import SBase
from binding import Binding
from event import Event
from handle_exception import handle_exception

class EventOpt(SBase):
    '''
    EventOpt Class
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(EventOpt, self).__init__()

        self.events = list()
        _modules = {
                'run_plugin'        :   'RunPlugin'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def event_opt(self, *args, **kargs):
        '''
        entry of event operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _new_event(self, config, level = 0, *args, **kargs):
        '''
        create new event and init its attributes
        '''
        _level  = config.get('level', 0)
        if level != _level and _level != 999:
            return
        _event  = Event()
        _data   = config.get('data', None)
        _event.name     = config['name']
        _event.handler  = config['handler']
        _event.data     = _data
        _event.level    = _level
        if 'params' in config and config['params']:
            _event.params   = config['params']
        return _event

    @handle_exception
    def _handle_event(self, event, *args, **kargs):
        '''
        handle event
        '''
        self.run_plugin(plugin=event.name, prefix='handle', event=event)
        event.done()

    @handle_exception
    def _handle_events(self, data, level = 0, *args, **kargs):
        '''
        loop events list and handle event
        '''
        for _event in self.events:
            if _event.is_done():
                continue
            elif _event.level == level or _event.level == 999:
                self._handle_event(_event)

    @handle_exception
    def _init_events(self, *args, **kargs):
        '''
        reset events
        '''
        for _event in self.events:
            _event.init()

    @handle_exception
    def _add_event(self, config, level = 0, *args, **kargs):
        '''
        enqueue event
        '''
        _event = self._new_event(config, level)
        if _event:
            self.events.append(_event)

    @handle_exception
    def _add_events(self, data, params = None, level = 0, *args, **kargs):
        '''
        enqueue event
        '''
        if data is None:
            return
        for _config in data:
            _config['params'] = params
            self._add_event(_config, level)

    @handle_exception
    def _results(self, *args, **kargs):
        '''
        return event results
        '''
        return [x.result for x in self.events if x.result]

    @handle_exception
    def _clear_events(self, *args, **kargs):
        '''
        clear events
        '''
        self.events = list()

    @handle_exception
    def _clear_results(self, *args, **kargs):
        '''
        clear events results
        '''
        for _event in self.events:
            _event.result = dict()
