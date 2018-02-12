# -*- coding: utf-8 -*-

import traceback

from singleton import Singleton

class _Times(Singleton):
    '''
    Control Exception output
    '''
    def __init__(self, *args, **kargs):
        super(_Times, self).__init__()
        self.times = 0

    def get_times(self):
        return self.times

    def inc_times(self):
        self.times += 1

def handle_exception(func):
    def func_wrapper(*args, **kargs):
        try:
            _result = func(*args, **kargs)
        except:
            _times = _Times()
            if _times.get_times() == 5:
                print traceback.format_exc()
            _times.inc_times()
            raise
        return _result
    return func_wrapper
