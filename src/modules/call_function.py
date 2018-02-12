# -*- coding:utf-8 -*-
'''
This Class is used to compose function call
'''
from singleton import Singleton
from binding import Binding
from handle_exception import handle_exception

class CallFunction(Singleton):
    '''
    Construct Call Function
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(CallFunction, self).__init__()

        _modules = {
                'convert'           :   'Convert'
                }

        Binding().binding(self, modules = _modules, entity = self)

        self.call_func(*args, **kargs)

    @handle_exception
    def _str_arg(self, data):
        return data.join(['"', '"'])

    @handle_exception
    def _to_kargs(self, data):
        _data = list()
        for _key, _value in data.items():
            if type(_value) is str:
                _data.append(self.convert(karg=(_key, self._str_arg(_value))))
            else:
                _data.append(self.convert(karg=(_key, _value)))
        return _data

    @handle_exception
    def _check_duplicate(self, args):
        '''
        Check if some key is duplicated to identify if we are running plugins
        '''
        _keys   = dict()
        for _index, _item in enumerate(args):
            if type(_item) is dict:
                for _key in _item:
                    if _key in _keys:
                        return 1
                    else:
                        _keys[_key] = 1

    @handle_exception
    def _to_args(self, args):
        '''
        Compose args from arguments list
        '''
        if not args:
            return None
        elif type(args) is dict:
            return str(args)
        elif self._check_duplicate(args):
            return args

        args = self.convert(to_list=args)
        for _index, _item in enumerate(args):
            if type(_item) is str:
                args[_index] = self._str_arg(_item)
            elif type(_item) is dict:
                args[_index] = self.convert(args=self._to_kargs(_item))
        return self.convert(args=args)

    @handle_exception
    def _to_func(self, func_name, instances):
        '''
        Select appropriated function from available class instances
        '''
        for _class in instances:
            _func = getattr(_class, func_name, None)
            if _func:
                return _func

    @handle_exception
    def call_func(self, *args, **kargs):
        '''
        call function with arguments
        '''
        if 'call_func' in kargs:
            (func_name, func_args, instances) = args

            _func = self._to_func(func_name, instances)
            _args = self._to_args(func_args)

            if type(_args) is str:
                return _func() if not _args else eval(_args.join(['_func(', ')']))

            for _item in _args:
                eval(self.convert(join = ['_func(', self._to_args([_item]), ')']))
