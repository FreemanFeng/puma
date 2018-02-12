# -*- coding:utf-8 -*-
'''
This Class is to convert data
'''
import os
import signal
import glob
from multiprocessing import Process, Queue

from binding import Binding
from singleton import Singleton
from handle_exception import handle_exception

class QueueOpt(Singleton):
    '''
    Class for Queue Operation
    '''
    (SHELL_PROCESS, FORK_PROCESS)= ('shell', 'fork')

    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(QueueOpt, self).__init__()

        _modules = {
                'inner_call'    :   'InnerCall',
                'convert'       :   'Convert'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def queue_opt(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _kill_pids(self, pids_queue, *args, **kargs):
        '''
        kill process id
        '''
        if pids_queue is None:
            return
        print "Killing Processes ..."
        while not pids_queue.empty():
            _pid = pids_queue.get()
            try:
                print "Killing Process %s ..." % _pid
                os.kill(_pid, signal.SIGTERM)
            except OSError as e:
                print "Exception in Killing :%s" % e
                continue

    @handle_exception
    def _store_pid(self, data, *args, **kargs):
        (pid, params) = data
        _path = params['pids_output']
        _ext  = kargs.get('ext', self.FORK_PROCESS)
        _name = self.convert(dot=(pid, _ext, 'pid'))
        _file = os.path.join(_path, _name)
        print "Saving pid %s to path %s ..." % (pid, _path)
        with open(_file, 'w') as f:
            f.write("%s" % pid)

    @handle_exception
    def _clear_pids(self, params, *args, **kargs):
        _path = params['pids_output']
        print "Killing Process from pids path %s ..." % _path
        for x in glob.glob(_path + '/*.pid'):
            _name   = os.path.basename(x)
            _parts  = _name.split('.')
            _pid    = int(_parts[0])
            _ext    = _parts[1]
            try:
                print "Killing Process %s ..." % _pid
                if _ext == self.SHELL_PROCESS:
                    os.killpg(os.getpgid(_pid), signal.SIGTERM)
                else:
                    os.killpg(_pid, signal.SIGKILL)
                    os.kill(_pid, signal.SIGTERM)
            except OSError as e:
                print "Exception in Killing :%s" % e
                continue

    @handle_exception
    def _test(self, params, *args, **kargs):
        '''
        测试专用
        '''
        self.queue_opt(store_pid=(4202, params))
        self.queue_opt(clear_pids=params)

if __name__ == '__main__':
    _obj = QueueOpt()
    _params = dict()
    _params['pids_output'] = '/home/share/codes/puma/testing/ucstart/data/pids'
    _obj.queue_opt(test=_params)
