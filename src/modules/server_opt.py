# -*- coding:utf-8 -*-
'''
This Class is to create simulated server, like U3,
Compress Center, Image Center, etc.
'''

import paramiko
import os
import sys
import signal
import traceback
from multiprocessing import Queue
import time
from datetime import datetime

from MBase import MBase
from config_manager import ConfigManager
from paths import Paths
from handle_exception import handle_exception

from twisted.web import server, resource
from twisted.internet import reactor, endpoints, protocol

class ServerOpt(MBase):
    '''
    Create Server Simulator
    '''
    _SRV_TIMEOUT = 0.5
    def __init__(self):
        '''
        init server instance
        '''
        super(ServerOpt, self).__init__()
        self.queue      = None
        self.pids_queue = None
        self.started    = None
        self.ssh_bins   = dict()
        self._callback  = {
                'http'  :   self._start_http_server,
                'tcp'   :   self._start_tcp_server,
                'ontcp' :   self._start_ontcp_server,
                'other' :   self._start_other_server
                }

    @handle_exception
    def _get_class(self, module_name, class_name):
        _cmd    = 'from %s import %s' % (module_name, class_name)
        exec _cmd in globals()
        return eval(class_name)

    @handle_exception
    def _split_name(self, name):
        return name.strip().split()

    @handle_exception
    def _build_class_name(self, name_parts):
        _parts = [self.convert(join=(x[0].upper(), x[1:])) for x in name_parts]
        _parts.append('Server')
        return self.convert(join=_parts)

    @handle_exception
    def _build_module_name(self, name_parts):
        _parts = [self.convert(join=(x[0].lower(), x[1:])) for x in name_parts]
        _parts.append('server')
        return self.convert(underscore=_parts)

    @handle_exception
    def _build_factory_name(self, proto, name_parts):
        if proto != 'ontcp':
            return None
        _parts = [self.convert(join=(x[0].upper(), x[1:])) for x in name_parts]
        _parts.append('Factory')
        return self.convert(join=_parts)

    @handle_exception
    def _start_socat_server(self, data, *args, **kargs):
        (server_config, pids_queue) = data
        _pid = os.getpid()
        if pids_queue is not None:
            pids_queue.put(_pid)
        _config = server_config['socat']
        _ssh    = self.ssh_opt(init_ssh=_config)
        _cmd    = server_config['cmd']
        self.ssh_opt(ssh_send=(_ssh, _cmd))

    @handle_exception
    def _kill_ssh_bins(self):
        for _name, _config in self.ssh_bins.items():
            _ssh = self.ssh_opt(init_ssh=_config)
            _cmd = "ps ux | grep %s | grep -v grep | sed 's/ \\+/ /g' | cut -d ' ' -f 2 | xargs kill -9" % _name
            _ret = self.ssh_opt(ssh_cmd=(_ssh, _cmd))
            self.logger.info(_ret)

    @handle_exception
    def _start_server(self, data, *args, **kargs):
        (server_config, pids_queue) = data
        _port           = server_config['port']
        _proto          = server_config['proto']
        _name           = server_config['name']
        _parts          = self._split_name(_name)
        _class_name     = self._build_class_name(_parts)
        _module_name    = self._build_module_name(_parts)
        _fact_name      = self._build_factory_name(_proto, _parts)
        _factory        = None
        _pid = os.getpid()
        if pids_queue is not None:
            pids_queue.put(_pid)
        _class = self._get_class(_module_name, _class_name)
        if _proto == 'ontcp':
            _factory = self._get_class(_module_name, _fact_name)
        if _proto != 'other':
            self._callback[_proto](_class, _port, _name, _factory, *args)
        else:
            self._callback[_proto](_class, *args)

    @handle_exception
    def _start_http_server(self, instance, port, name, *args):
        self.logger.info("Starting %s (via HTTP) on port %d" % (name, port))
        endpoints.serverFromString(reactor,
                "tcp:%s" % str(port)).listen(server.Site(instance()))
        reactor.run()
        self.logger.info("%s listening port %d released" % (name, port))

    @handle_exception
    def _start_tcp_server(self, instance, port, name, *args):
        self.logger.info("Starting %s (via TCP) on port %d" % (name, port))
        _factory = protocol.ServerFactory()
        _factory.protocol = instance
        reactor.listenTCP(port, _factory)
        reactor.run()
        self.logger.info("%s listening port %d released" % (name, port))

    @handle_exception
    def _start_ontcp_server(self, instance, port, name, factory, *args):
        self.logger.info("Starting %s (via TCP) on port %d" % (name, port))
        reactor.listenTCP(port, factory())
        reactor.run()
        self.logger.info("%s listening port %d released" % (name, port))

    @handle_exception
    def _start_other_server(self, instance, *args, **kargs):
        return instance().run(self.queue)

    @handle_exception
    def _run_ssh(self, config):
        _ssh        = config['ssh']
        _cmd        = config['cmd']
        _sleep      = config['sleep']
        self.logger.info('Delay Run SSH: %s' % _cmd)
        self.ssh_opt(ssh_send=(_ssh, _cmd))
        time.sleep(_sleep)

    @handle_exception
    def _set_timeout(self, config):
        _timeout = self._SRV_TIMEOUT
        if 'timeout' in config:
            _timeout = float(config['timeout'])
        elif self.cm.timeout:
            _timeout = self.cm.timeout
        return _timeout

    @handle_exception
    def _port_occupied(self, config, ports):
        _port = config['port']
        if _port in ports and type(_port) is int:
            return True
        ports[_port] = 1
        return False

    @handle_exception
    def _wrap_process(self, config, *args, **kargs):
        '''
        run simulated server
        '''
        _ports          = dict()
        self.queue      = Queue()
        self.pids_queue = Queue(len(self.cm.server))
        for _index, _server_config in enumerate(self.cm.server):
            if _index == len(self.cm.server) - 1:
                self._start_server((_server_config, None), *args)

            elif 'ssh' in _server_config:
                self._run_ssh(_server_config)

            elif 'socat' in _server_config:
                _cmd    = _server_config['cmd']
                _bin    = os.path.basename(_server_config['bin'])
                _config = _server_config['socat']
                self.ssh_bins[_bin] = _config
                self.logger.info('Run SOCAT: %s' % _cmd)
                self.start_proc(self._SRV_TIMEOUT,
                                self._start_socat_server,
                                self.queue,
                                _server_config,
                                self.pids_queue)

            elif not self._port_occupied(_server_config, _ports):
                self.logger.info('Starting Server with Config %s' % _server_config)
                _timeout = self._set_timeout(_server_config)
                self.start_proc(_timeout,
                                self._start_server,
                                self.queue,
                                _server_config,
                                self.pids_queue,
                                *args)

    @handle_exception
    def get_queue(self):
        return self.queue

    @handle_exception
    def start_server(self, config, *args, **kargs):
        '''
        start server
        '''
        self.load_config()
        for _server_config in self.cm.server:
            self._start_server((_server_config, None), *args)
            return

    @handle_exception
    def start_multi_server(self, config, *args, **kargs):
        '''
        start server
        '''
        self.load_config()
        ############################
        ## debug use, single process
        ############################
        #for _server_config in self.cm.server:
        #    self._start_server((_server_config, None), *args)
        if not self.started:
            self._wrap_process(config, *args)
        self.started = 1

    @handle_exception
    def clear_procs(self):
        self._kill_ssh_bins()
        #+=========================
        #| 1. 清除子进程
        #+=========================
        self.queue_opt(clear_pids=self.cm.global_config)
        #+=========================
        #| 2. 清除主进程
        #+=========================
        self.queue_opt(kill_pids=self.pids_queue)
