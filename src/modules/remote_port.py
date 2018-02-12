# -*- coding:utf-8 -*-

import socket
import random

from SBase import SBase
from handle_exception import handle_exception

class RemotePort(SBase):
    def __init__(self, *args, **kargs):
        super(RemotePort, self).__init__()
        self._ports = dict()

    @handle_exception
    def remote_port(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    def _is_occupied(self, data, *args, **kargs):
        (host, port) = data
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _sock.settimeout(1)
        try:
            _sock.connect((host, int(port)))
            _sock.close()
        except:
            return False
        self.logger.info("Port %s occupied!" % port)
        return True

    def _select_port(self, host, minval, maxval):
        _port   = random.randint(minval, maxval)
        _tries  = 0
        while self.remote_port(is_occupied=(host, _port)):
            _port   = random.randint(minval, maxval)
            _tries += 1
            if _tries > 20:
                self.logger.info("[FATAL ERROR]Allocate Port Failed!")
                return 0
        return _port

    def _get(self, data, *args, **kargs):
        (host, name, cnt, minval, maxval) = data
        _key = self.convert(join=(name, cnt))
        if _key not in self._ports:
            self._ports[_key] = self._select_port(host, minval, maxval)
        return self._ports[_key]

    def _update(self, data, *args, **kargs):
        (host, name, cnt, minval, maxval) = data
        _key = self.convert(join=(name, cnt))
        self._ports[_key] = self._select_port(host, minval, maxval)
        return self._ports[_key]

if __name__ == '__main__':
    _obj = RemotePort()
    for index in range(20):
        print _obj.remote_port(get=('127.0.0.1', 'Test Server', index))
