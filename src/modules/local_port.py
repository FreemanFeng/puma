# -*- coding:utf-8 -*-

import socket
import random

from SBase import SBase
from handle_exception import handle_exception

class LocalPort(SBase):
    def __init__(self, *args, **kargs):
        super(LocalPort, self).__init__()
        self._ports = dict()

    @handle_exception
    def local_port(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    def _is_occupied(self, port, *args, **kargs):
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _sock.bind(('127.0.0.1', int(port)))
        except:
            self.logger.info("Port %s occupied!" % port)
            _sock.close()
            return True
        _sock.close()
        return False

    def _select_port(self, minval, maxval):
        _port   = random.randint(minval, maxval)
        _tries  = 0
        while self._is_occupied(_port):
            _port   = random.randint(minval, maxval)
            _tries += 1
            if _tries > 20:
                self.logger.info("[FATAL ERROR]Allocate Port Failed!")
                return 0
        return _port

    def _get(self, data, *args, **kargs):
        (name, cnt, minval, maxval) = data
        _key = self.convert(join=(name, cnt))
        if _key not in self._ports:
            self._ports[_key] = self._select_port(minval, maxval)
        return self._ports[_key]

    def _update(self, data, *args, **kargs):
        (name, cnt, minval, maxval) = data
        _key = self.convert(join=(name, cnt))
        self._ports[_key] = self._select_port(minval, maxval)
        return self._ports[_key]

if __name__ == '__main__':
    _obj = LocalPort()
    for index in range(20):
        print _obj.local_port(get=('Test Server', index))
