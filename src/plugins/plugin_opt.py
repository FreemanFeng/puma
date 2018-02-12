# -*- coding:utf-8 -*-
'''
This Class is used to perform operation
'''
import os
import re

from plugin import Plugin
from binding import Binding
from plugin_base import PluginBase
from handle_exception import handle_exception

class PluginOpt(PluginBase):
    '''
    Plugin for operation
    '''
    def __init__(self, *args, **kargs):
        '''
        binding some modules in init stage
        '''
        super(PluginOpt, self).__init__(*args, **kargs)
        self._callback  = dict()
        self.plugin     = Plugin()

    @handle_exception
    def _do_opt(self, config, *args, **kargs):
        '''
        should be implemented by child class
        '''
        pass

    @handle_exception
    def _save_data(self, *args, **kargs):
        '''
        should be implemented by child class
        '''
        pass

    @handle_exception
    def process_result(self, *args, **kargs):
        '''
        should be implemented by child class
        '''
        pass

    @handle_exception
    def _get_attr(self, name, *args, **kargs):
        return getattr(self, name, None)

    @handle_exception
    def _fill_events(self, events, *args, **kargs):
        if events is None:
            return
        for _event in events:
            _name       = _event.get('name', None)
            _handler    = _event.get('handler', None)
            _data       = _event.get('data', None)
            if _name is None and _handler is None and type(_data) is list:
                _event['name'] = 'events'
                _event['handler'] = 'set_levels'
            elif _handler is None:
                _event['name'] = 'events'
                _event['handler'] = 'set_events'
                _event['level'] = 999
            elif _name is None:
                _event['name'] = 'events'

    @handle_exception
    def _process_events(self, config, *args, **kargs):
        '''
        loop events and process results
        '''
        _events = None
        self.events = config
        self._fill_events(self.events)
        _results = self.loop_events(*args, **kargs)
        _events = self.process_results(_results, *args, **kargs)
        self.event_opt(clear_events=1)
        if _events:
            self._process_events(_events, *args, **kargs)

    @handle_exception
    def main_do_opt(self, config, *args, **kargs):
        '''
        Perform operation, i.e. start, stop, etc.
        '''
        _levels = config.get('levels', 1)
        self._process_events(config)
        for _level in range(_levels):
            self._process_events(config, level = _level + 1)

    @handle_exception
    def main_process_result(self, result, *args, **kargs):
        '''
        process single event result
        '''
        for _key, _value in result.items():
            self.params[_key] = _value
            if _key in self._callback:
                self._callback[_key]()

    @handle_exception
    def process_results(self, results, *args, **kargs):
        '''
        process result
        '''
        _events = list()
        for _result in results:
            if 'events' in _result:
                _events.extend(_result['events'])
            else:
                self.process_result(_result)
        return _events

    @handle_exception
    def handle_events(self, *args, **kargs):
        '''
        handle events
        '''
        return super(PluginOpt, self).main_handle_events(*args, **kargs)

    @handle_exception
    def loop_events(self, *args, **kargs):
        '''
        loop events
        '''
        return super(PluginOpt, self).main_loop_events(*args, **kargs)

