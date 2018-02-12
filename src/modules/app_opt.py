# -*- coding:utf-8 -*-

import json
import os
from time import time
import re
from multiprocessing import Queue

from SBase import SBase
from binding import Binding
from handle_exception import handle_exception

class AppOpt(SBase):
    def __init__(self, *args, **kargs):
        super(AppOpt, self).__init__()
        self._callback = {
                'android'   :   self._build_android_cmds,
                'ios'       :   self._build_ios_cmds,
                }
        _modules = {
                'proc_opt'  :   'ProcOpt',
                'queue_opt' :   'QueueOpt'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def app_opt(self, *args, **kargs):
        '''
        本类的唯一导出接口
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _build_android_cmds(self, params, configs):
        _cmds = list()
        for _config in configs:
            _cmd = _config
            for _key, _val in params.items():
                _cmd = re.sub(_key, _val, _cmd)
            _cmds.append(_cmd)
        return _cmds

    @handle_exception
    def _build_ios_cmds(self, params, configs):
        _cmds = list()
        for _config in configs:
            _cmd = _config
            for _key, _val in params.items():
                _cmd = re.sub(_key, _val, _cmd)
            _cmds.append(_cmd)
        return _cmds

    @handle_exception
    def _build_cmds(self, data, *args, **kargs):
        (params, action) = data
        _platform   = params['platform']
        _app        = self.cm.app[_platform]
        if _platform not in params:
            _node = dict()
            _node.update(params)
            params[_platform] = dict()
            params[_platform].update(_node)
        return self._callback[_platform](params[_platform], _app[action])

    @handle_exception
    def _start(self, params, *args, **kargs):
        '''
        启动App
        '''
        if int(params['debug_device']) == 1:
            self._init(params)
        else:
            self._connect(params)
        _cmds = self.app_opt(build_cmds=(params, 'start'))
        #_ret = self.shell_opt(runs = (_cmds, params), cli = 1)
        _ret = self.shell_opt(cmds = _cmds, cli = 1)
        self.logger.info(_ret)

    @handle_exception
    def _stop(self, params, *args, **kargs):
        '''
        关闭App
        '''
        if int(params['debug_device']) == 1:
            self._init(params)
        else:
            self._connect(params)
        _cmds = self.app_opt(build_cmds=(params, 'stop'))
        #_ret = self.shell_opt(runs = (_cmds, params))
        _ret = self.shell_opt(cmds = _cmds)
        #self.logger.info(_ret)

    @handle_exception
    def _init(self, params, *args, **kargs):
        '''
        初始化App
        '''
        _cmds = self.app_opt(build_cmds=(params, 'init'))
        #self.logger.info(_cmds)
        #_ret = self.shell_opt(runs = (_cmds, params))
        _ret = self.shell_opt(cmds = _cmds)
        #self.logger.info(_ret)

    @handle_exception
    def _connect(self, params, *args, **kargs):
        '''
        初始化App
        '''
        _cmds = self.app_opt(build_cmds=(params, 'connect'))
        #_ret = self.shell_opt(runs = (_cmds, params))
        _ret = self.shell_opt(cmds = _cmds)
        #self.logger.info(_ret)

    @handle_exception
    def _install(self, params, *args, **kargs):
        '''
        安装App
        '''
        if int(params['debug_device']) == 1:
            self._init(params)
        else:
            self._connect(params)
        _cmds = self.app_opt(build_cmds=(params, 'install'))
        _ret = self.shell_opt(runs = (_cmds, params))
        #_ret = self.shell_opt(cmds = _cmds)
        #self.logger.info(_ret)

    @handle_exception
    def _app_install(self, data, *args, **kargs):
        '''
        安装App
        '''
        (params, queue) = data
        #self.queue_opt(store_pid=(os.getpid(), params))
        self._install(params)
        queue.put(params['serial'])

    @handle_exception
    def _timeout_trigger(self, data, *args, **kargs):
        '''
        超时触发器
        '''
        (timeout, queue) = data
        sleep(timeout)
        queue.put(1)

    @handle_exception
    def _post_install(self, data, *args, **kargs):
        '''
        多进程安装App
        '''
        (params, queue) =data
        _serials = list()
        _start  = time()
        _timeout = self.cm.app_timeout['install']
        for _item in params['devices']:
            _serial = queue.get()
            if _serial == 1:
                self.logger.info('Waiting installation Timeout')
                break
            _serials.append(_serial)
            if time() - _start > _timeout:
                break
        self.queue_opt(clear_pids=params)
        assert len(_serials) > 0, "No devices successfully installed UC!"
        self.logger.info('Devices %s installed UC successfully' % _serials)
        _devices = dict()
        _params = params['devices']
        for _serial in _serials:
            _devices[_serial] = dict()
            _devices[_serial].update(_params[_serial])
        _params = dict()
        _params.update(_devices)

    @handle_exception
    def _multi_install(self, params, *args, **kargs):
        '''
        多进程安装App
        '''
        _queue = Queue()
        self._init(params)
        self.logger.info(params)
        _timeout = self.cm.app_timeout['install']
        self.start_proc(0, self._timeout_trigger, _queue, _timeout, _queue)
        for _serial, _config in params['devices'].items():
            _params = dict()
            _params.update(params)
            _platform = _params['platform']
            _node = _params[_platform]
            _node.update(_config)
            _params['serial'] = _serial
            #self._app_install((_params, _queue))
            #self._install(_params)
            self.start_proc(0, self._app_install, _queue, _params, _queue)
        self.app_opt(post_install=(params, _queue))


    @handle_exception
    def _uninstall(self, params, *args, **kargs):
        '''
        卸载App
        '''
        _cmds = self.app_opt(build_cmds=(params, 'uninstall'))
        _ret = self.shell_opt(cmds = _cmds)
        self.logger.info(_ret)

    @handle_exception
    def _app_uninstall(self, data, *args, **kargs):
        '''
        卸载App
        '''
        (params, queue) = data
        self._uninstall(params)
        queue.put(1)

    @handle_exception
    def _multi_uninstall(self, params, *args, **kargs):
        '''
        多进程安装App
        '''
        _queue = Queue()
        _count = 0
        for _serial, _config in params['devices'].items():
            for _id, _device in _config.items():
                _params = dict()
                _params.update(params)
                _platform = _params['platform']
                _node = _params[_platform]
                _node['device_name'] = _device
                #self._uninstall(params)
                self.start_proc(0, self._app_uninstall, _queue, _params, _queue)
                _count += 1
        for _item in range(_count):
            _queue.get()

    @handle_exception
    def _test(self, *args, **kargs):
        '''
        测试专用
        '''
        #self.app_opt(stop=1)
        #time.sleep(5)
        #self.app_opt(start=self.cm.params)
        #_cmds = self.app_opt(build_cmds=(self.cm.params, 'start'))
        #_cmds = self.app_opt(build_cmds=(self.cm.params, 'install'))
        #_cmds = self.app_opt(build_cmds=(self.cm.params, 'uninstall'))
        _cmds = self.app_opt(build_cmds=(self.cm.params, 'stop'))
        self.logger.info(_cmds)
        #time.sleep(16)
        #self.app_opt(stop=1)

if __name__ == '__main__':
    _obj = AppOpt()
    _obj.cm.load_yaml('etc/apps/ucstart/ucstart_config.yml')
    _obj.cm.params = dict()
    _obj.cm.params['platform'] = 'android'
    _obj.cm.params['android'] = {
            'package_name'  :   'com.UCMobile',
            'activity_name' :   'com.UCMobile.main.UCMobile',
            'device_name'   :   'f49ff3e78dee',
            'apk_name'      :   'UCBrowser_V11.7.9.959_android_pf145_Build171214174449.apk'
            }
    _obj.app_opt(test=1)
