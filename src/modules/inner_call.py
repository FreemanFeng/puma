# -*- coding:utf-8 -*-
'''
This Class is used to compose function call
'''
from singleton import Singleton
from handle_exception import handle_exception

class InnerCall(Singleton):
    '''
    Construct Call Inner
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(InnerCall, self).__init__()
        self.inner_call(*args, **kargs)

    @handle_exception
    def inner_call(self, entity=None, *args, **kargs):
        '''
        call function with '_' as prefix
        '''
        for key in kargs:
            _entity = entity if entity else self
            _func = getattr(_entity, ''.join(['_', key]), None)
            if _func:
                return _func(kargs[key], *args, **kargs)
