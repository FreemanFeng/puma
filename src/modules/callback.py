# -*- coding:utf-8 -*-
'''
This Class is to set callback functions as attributes
'''
import os
import os.path
from singleton import Singleton
from handle_exception import handle_exception

class Callback(Singleton):
    '''
    Binding Callback Functions
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(Callback, self).__init__()

        self.add_callbacks(*args, **kargs)

    @handle_exception
    def add_callbacks(self, *args, **kargs):
        if 'callback' in kargs:
            _callback = kargs['callback']
            _entity = self if 'entity' not in kargs else kargs['entity']
            for name, attr in _callback.items():
                _entity.__setattr__(name, attr)
