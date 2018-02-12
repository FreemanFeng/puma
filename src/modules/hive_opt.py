# -*- coding:utf-8 -*-

import json
import os
import time

import requests
from binding import Binding
from SBase import SBase
from handle_exception import handle_exception
#TODO Debug For APP install / uninstall
from app_opt import AppOpt

class HiveOpt(SBase):
    def __init__(self, *args, **kargs):
        super(HiveOpt, self).__init__()
        _modules = {
                'http_opt'  :   'HttpOpt'
                }
        Binding().binding(self, modules = _modules, entity = self)
        self.cm.load_yaml('etc/protocol/hive.yml')
        self.devices = dict()

    @handle_exception
    def hive_opt(self, *args, **kargs):
        '''
        本类的唯一导出接口
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _hive_headers(self):
        '''
        Hive请求头
        '''
        _token = self.cm.hive['token']
        _headers = dict()
        _headers['Authorization'] = self.convert(join=('Bearer ', _token))
        _headers['Content-Type'] = 'application/json'
        return _headers

    @handle_exception
    def _request(self, url, method = 'get', data = None):
        '''
        Hive请求
        '''
        _headers = self._hive_headers()
        _url = self.convert(join=(self.cm.hive['api'], url))
        _req = requests.request(method, _url, json = data,  headers = _headers)
        if _req.text:
            return json.loads(_req.text)
        return _req.text

    @handle_exception
    def _devices(self, *args, **kargs):
        '''
        获取所有的设备信息,包括在线和不在线的设备
        '''
        return self._request('devices')

    @handle_exception
    def _device(self, serial, *args, **kargs):
        '''
        获取特定设备的信息
        '''
        _url = self.convert(join=('devices/', serial))
        return self._request(_url)

    @handle_exception
    def _user(self, *args, **kargs):
        '''
        获取当前认证用户的信息
        '''
        return self._request('user')

    @handle_exception
    def _user_devices(self, *args, **kargs):
        '''
        获取当前认证用户正在使用的设备的信息
        '''
        return self._request('user/devices')

    @handle_exception
    def _add_device(self, data, *args, **kargs):
        '''
        把serial对应的手机加入到当前认证用户下
        '''
        (serial, timeout) = data
        if timeout is None:
            timeout = 3600 * 1000
        _body = dict()
        _body['serial']  = serial
        _body['timeout'] = timeout
        return self._request('user/devices', 'post', _body)

    @handle_exception
    def _delete_device(self, serial, *args, **kargs):
        '''
        把serial对应的手机从当前认证用户中删除
        '''
        _url = self.convert(join=('user/devices/', serial))
        return self._request(_url, 'delete')

    @handle_exception
    def _get_connect(self, serial, *args, **kargs):
        '''
        获取特定手机的远程调试url
        '''
        _url = self.convert(join=('user/devices/', serial, '/remoteConnect'))
        return self._request(_url, 'post')

    @handle_exception
    def _get_device(self, platform, *args, **kargs):
        '''
        获取可用手机,若有返回第一个，否则返回None
        '''
        _all    = self.hive_opt(devices=1)
        _list   = {x:1 for x in self.cm.hive['provider']}
        _black  = {x:1 for x in self.cm.hive['blacklist']}
        if _all and 'devices' in _all:
            for _device in _all['devices']:
                if 'platform' not in _device:
                    continue
                #if platform.lower() != _device['platform'].lower():
                #    continue
                # TODO hive手机目前只支持android
                if 'android' != _device['platform'].lower() and 'ios' != _device['platform'].lower():
                    continue
                if _device['provider']['name'] not in _list:
                    continue
                # TODO 跳过有问题的机型
                if _device['serial'] in _black:
                    continue
                if _device['phone']['imei'] is None:
                    continue
                #TODO 暂时绕过权限允许问题
                _ver = _device.get('version', '0')
                if int(_ver[0]) >= 6:
                    continue
                _present    = _device['present']
                _ready      = _device['ready']
                _owner      = _device['owner']
                if _present and _ready and _owner is None:
                    self.logger.info('Got Device: %s' % _device['serial'])
                    return _device['serial']
        return None

    @handle_exception
    def _apply_devices(self, data, *args, **kargs):
        '''
        申请可用设备
        '''
        (count, params) = data
        _black = dict()
        for _index in range(count):
            _serial = self.hive_opt(get_device=params['platform'])
            if _serial in _black:
                break
            if _serial:
                self.hive_opt(add_device=(_serial, None))
                _conn   = self.hive_opt(get_connect=_serial)
                self.logger.info(_conn)
                if 'remoteConnectUrl' not in _conn:
                    self.logger.info('Device %s Not Availabled' % _serial)
                    _black[_serial] = 1
                    continue
                _info   = self.hive_opt(device=_serial)
                _phone  = _info['device']['phone']
                self.devices[_serial] = {
                        'device_name' : _conn['remoteConnectUrl'],
                        'imei'        : _phone['imei'].strip(),
                        'mac'         : _phone['mac'].upper().replace(' ', '')
                        }

        self.logger.info('Applied Devices %s' % self.devices)
        assert len(self.devices) > 0, 'No Available Devices could be applied!'
        return self.devices

    @handle_exception
    def _return_devices(self, *args, **kargs):
        '''
        退还所有设备
        '''
        for _serial in self.devices:
            _ret = self.hive_opt(delete_device=_serial)
            self.logger.info(_ret)
        self.devices = dict()

    @handle_exception
    def _test(self, *args, **kargs):
        '''
        测试专用
        '''
        self.hive_opt(apply_devices=2)
        time.sleep(10.0)
        self.hive_opt(return_devices=2)
        #_devices = self.hive_opt(devices=1)
        #self.logger.info(_devices)

if __name__ == '__main__':
    _obj = HiveOpt()
    _obj.cm.load_yaml('etc/apps/ucstart/ucstart_config.yml')
    _params = dict()
    _params['platform'] = 'android'
    _devices = _obj.hive_opt(apply_devices=(2, _params))
    _app = AppOpt()
    _params['android'] = {
            'package_name'  :   'com.UCMobile',
            'activity_name' :   'com.UCMobile.main.UCMobile',
            'device_name'   :   'f49ff3e78dee',
            'apk_name'      :   '/innova/tmp/UCBrowser_V11.7.9.959_android_pf145_Build171216163906.apk'
            }
    #_app.app_opt(multi_uninstall=(_devices, _params))
    _app.app_opt(multi_install=(_devices, _params))
