# -*- coding:utf-8 -*-
'''
This Class is to run shell commands
'''
import sys
import os
import signal
import subprocess
import time
from multiprocessing import Queue

from SBase import SBase
from singleton import Singleton
from binding import Binding
from handle_exception import handle_exception

class ShellOpt(Singleton):
    '''
    Singleton class for Shell Operation Functions
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize shell_commands instance
        '''
        super(ShellOpt, self).__init__()
        _modules = {
                'inner_call'    :   'InnerCall',
                'proc_opt'      :   'ProcOpt',
                'queue_opt'     :   'QueueOpt'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def shell_opt(self, *args, **kargs):
        '''
        unique interface for http operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _cmds(self, data, *args, **kargs):
        '''
        execute shell commands with process
        '''
        _results = list()
        for _cmd in data:
            _ret = self.shell_opt(cmd = _cmd)
            _results.append(_ret)
        return _results

    def _cmd(self, data, *args, **kargs):
        """
        Runs command
        """
        return self._run((data, None), *args, **kargs)

    @handle_exception
    def _runs(self, data, *args, **kargs):
        '''
        execute shell commands with process
        '''
        (cmds, params) = data
        _results = list()
        print params
        for _cmd in cmds:
            _ret = self._run((_cmd, params), *args, **kargs)
            _results.append(_ret)
        return _results

    def _run(self, data, *args, **kargs):
        """
        Runs command in limited time
        """
        (cmd, params) = data
        print params
        stdout  = subprocess.PIPE if 'cli' in kargs else None
        stderr  = subprocess.PIPE if 'cli' in kargs else None
        popen   = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=stdout,
                                   stderr=stderr,
                                   preexec_fn=os.setsid)

        if params is not None:
            self.queue_opt(store_pid=(popen.pid, params), ext = 'shell')

        (stdout, stderr) = popen.communicate()

        result = {'returncode': popen.returncode,
                  'cmd': cmd,
                  'stdout': stdout,
                  'stderr': stderr}

        if popen.returncode == 2:
            raise _BashException(result)

        return result

    def _test(self, *args, **kargs):
        """
        测试专用
        """
        _cmd = '/vobs/tools/caddy/bin/caddy -port 54444'
        _params = dict()
        _params['pids_output'] = '/vobs/cache/tmp/pids'
        if not os.path.isdir(_params['pids_output']):
            os.makedirs(_params['pids_output'])
        _queue = Queue()
        self.start_proc(0, self._run, _queue, _cmd, _params)
        time.sleep(60.0)
        self.queue_opt(clear_pids=_params)
        time.sleep(60.0)
        print 'HAHAHA'
        #pass

class _BashException(Exception):
    """
    Exception handling for bash cmd
    """
    def __init__(self, result):
        Exception.__init__(self)
        self.result = result
        print >> sys.stderr, result

    def __str__(self):
        return "%s" % self.result

if __name__ == '__main__':
    _obj = ShellOpt()
    _obj.shell_opt(test = 1)
