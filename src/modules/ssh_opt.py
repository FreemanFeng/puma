# -*- coding:utf-8 -*-
'''
This Class is to create SSH connections
'''

import paramiko
import os
import time

from binding import Binding
from singleton import Singleton
from handle_exception import handle_exception

class SSHOpt(Singleton):
    '''
    Create SSH Connection
    '''
    def __init__(self):
        '''
        init ssh client
        '''
        super(SSHOpt, self).__init__()
        _modules = {
                'inner_call'    :   'InnerCall'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def ssh_opt(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    def _connect(self, client, config):
        '''
        connect to ssh host
        '''
        return client.connect(config['server'], config['port'], config['user'])

    @handle_exception
    def _init_ssh(self, config, *args, **kargs):
        '''
        init ssh client
        '''
        _client = paramiko.SSHClient()

        _client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self._connect(_client, config)

        #_tran   = _client.get_transport()
        #_tran.set_keepalive(1)

        return _client

    @handle_exception
    def _init_sftp(self, client, *args, **kargs):
        '''
        init ssh client
        '''
        return client.open_sftp()

    @handle_exception
    def _ssh_send(self, data, *args, **kargs):
        '''
        send ssh commands
        '''
        (client, cmd) = data

        client.exec_command(cmd)

    @handle_exception
    def _ssh_cmd(self, data, *args, **kargs):
        '''
        send ssh commands
        '''
        (client, cmd) = data

        (_stdin, _stdout, _stderr)= client.exec_command(cmd)

        _status = _stdout.channel.recv_exit_status()

        stdout = _stdout.readlines()
        stderr = _stderr.readlines()
        _result = { 'returncode' : _status,
                    'stdout' : stdout,
                    'stderr': stderr}

        return _result

    @handle_exception
    def _sftp_get(self, data, *args, **kargs):
        '''
        get file via ssh
        '''
        (sftp, remote, local) = data

        return sftp.get(remote, local)

    @handle_exception
    def _sftp_put(self, data, *args, **kargs):
        '''
        put file via ssh
        '''
        (sftp, local, remote) = data

        return sftp.put(local, remote)

    @handle_exception
    def _close_sftp(self, sftp, *args, **kargs):
        '''
        close sftp connection
        '''
        sftp.close()

    @handle_exception
    def _close_ssh(self, client, *args, **kargs):
        '''
        close ssh connection
        '''
        client.close()

if __name__ == '__main__':
    _obj = SSHOpt()
    _config = dict()
    _config['server'] = '100.84.72.192'
    _config['port'] = 9922
    _config['user'] = 'freeman'
    _ssh = _obj.ssh_opt(init_ssh=_config)
    _ret = _obj.ssh_opt(ssh_cmd=(_ssh,'ls'))
    print _ret
