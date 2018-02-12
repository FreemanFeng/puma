# -*- coding:utf-8 -*-
'''
This Class is to send sockets
'''
import socket
import time

from binding import Binding
from singleton import Singleton
from handle_exception import handle_exception

class SockOpt(Singleton):
    '''
    Class for Socket Operation
    '''
    def __init__(self, *args, **kargs):
        '''
        Call sock opt by default
        '''
        super(SockOpt, self).__init__()
        _modules = {
                'inner_call'    :   'InnerCall',
                'convert'       :   'Convert'
                }

        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def sock_opt(self, *args, **kargs):
        '''
        unique interface for sock operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _init_sock(self, *args, **kargs):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @handle_exception
    def _send(self, config, *args, **kargs):
        '''
        send message via socket
        '''
        (sock, server, port, message) = config
        sock.connect((server, int(port)))
        sock.send(message)

    @handle_exception
    def _receive(self, config, *args, **kargs):
        '''
        receive message via socket
        '''
        (sock, size) = config
        return sock.recv(size)

    @handle_exception
    def _close(self, sock, *args, **kargs):
        '''
        close socket
        '''
        sock.close()

if __name__ == '__main__':
    _obj = SockOpt()
    _sock = _obj.sock_opt(init_sock=1)
    _obj.sock_opt(send=(_sock, '100.84.72.192', 56060, 'HAHAHAHA'))
    _obj.sock_opt(receive=(_sock, 1024))
    #_obj.sock_opt(close=_sock)
