# -*- coding:utf-8 -*-
'''
This Class is to convert data
'''
from multiprocessing import Process, Queue

from binding import Binding
from singleton import Singleton
from handle_exception import handle_exception

class ProcOpt(Singleton):
    '''
    Class for Process Execution
    '''
    _KILL_MSG = "Process still running, will kill it"
    _TIME_OUT = 0.5

    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(ProcOpt, self).__init__()

        _modules = {
                'inner_call'    :   'InnerCall'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def proc_opt(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def proc_wrapper(self, func, queue, *args, **kargs):
        '''
        wrap process for running testcase
        '''
        func(*args, **kargs)

    @handle_exception
    def fork_proc(self, func, queue, *args, **kargs):
        '''
        Fork a new process
        '''
        return Process(target = self.proc_wrapper,
                       args = (func, queue, args, kargs))

    @handle_exception
    def start_proc(self, timeout, *args, **kargs):
        '''
        Run process until timeout
        '''
        _proc       = self.fork_proc(*args)
        _timeout    = timeout if timeout >= self._TIME_OUT else self._TIME_OUT
        _proc.start()
        _proc.join(_timeout)
        return _proc

    @handle_exception
    def kill_proc(self, proc, queue, log, *args, **kargs):
        '''
        Kill process
        '''
        print log
        proc.terminate()

    @handle_exception
    def run_proc(self, timeout, func, queue, *args, **kargs):
        '''
        Run process until timeout
        '''
        _proc = self.start_proc(timeout, func, queue, *args, **kargs)
        if _proc:
            self.kill_proc(_proc, queue, ProcOpt._KILL_MSG)

    @handle_exception
    def _run(self, data, *args, **kargs):
        '''
        Run process until timeout
        '''
        (timeout, func, queue) = data
        return self.run_proc(timeout, func, queue, *args, **kargs)
