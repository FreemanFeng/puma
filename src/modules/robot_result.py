# -*- coding:utf-8 -*-

from SBase import SBase
from handle_exception import handle_exception

class RobotResult(SBase):
    def __init__(self, *args, **kargs):
        super(RobotResult, self).__init__()
        self.queue = None

    @handle_exception
    def init_result(self, ret_type):
        if self.cm.results is None or type(self.cm.results) is not dict:
            self.cm.results = dict()
        if ret_type not in self.cm.results:
            self.cm.results[ret_type] = dict()

    @handle_exception
    def set_result(self, ret_type, key, value):
        self.init_result(ret_type)
        _type = self.cm.results[ret_type]
        _type[key] = value
        self.update_queue(self.cm.results)

    @handle_exception
    def update_result(self, ret_type, data):
        self.init_result(ret_type)
        self.cm.results[ret_type].update(data)
        self.update_queue(self.cm.results)

    def _update_results(self):
        _results = self.queue.get()
        if _results and type(_results) is dict:
            _results.update(self.cm.results)
            self.cm.results.update(_results)

    @handle_exception
    def update_queue(self, results):
        if self.queue is not None:
            if not self.queue.empty():
                #self.logger.info('POP queue')
                self._update_results()
            self.queue.put(self.cm.results)
            #self.logger.info('Put in queue')

    @handle_exception
    def set_queue(self, queue):
        self.queue = queue
