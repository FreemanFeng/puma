# -*- coding:utf-8 -*-
'''
This Class is to set binding functions as attributes
'''
import os
import os.path
import inspect

from singleton import Singleton
from handle_exception import handle_exception

class Binding(Singleton):
    '''
    Binding Attributes
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize binding instance
        '''
        super(Binding, self).__init__()

        self.binding(*args, **kargs)

    @handle_exception
    def binding(self, *args, **kargs):
        '''
        binding modules class methods
        '''
        if 'modules' in kargs:
            _modules = kargs['modules']
            _entity = kargs.get('entity', self)
            for _module_name, _class_name in _modules.iteritems():
                _cmd = 'from %s import %s' %(_module_name, _class_name)
                exec _cmd in globals()
                _class = eval(_class_name)()
                self._set_members(_entity, _class)

    def _set_members(self, entity, class_obj):
        '''
        set members
        '''
        for _name, _value in inspect.getmembers(class_obj, callable):
            self._add_member(entity, _name, _value)

    def _add_member(self, entity, name, value):
        '''
        add member
        '''
        if name[0] != '_':
            entity.__setattr__(name, value)
