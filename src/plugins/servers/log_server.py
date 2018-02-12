# -*- coding: utf-8 -*-

import os
import json
from time import time, strftime, localtime
from datetime import datetime

from twisted.web import server, resource
from twisted.internet import reactor, endpoints, tcp

from plugin_log import PluginLog

class LogServer(resource.Resource):
    '''
    twisted api: http://twistedmatrix.com/documents/current/api/
    http://twistedmatrix.com/documents/current/api/nameIndex.html#R
    http://twistedmatrix.com/documents/current/api/twisted.web.http.Request.html
    '''
    isLeaf  = True
    plugin  = PluginLog()
    #config  = dict()
    config  = {
            'tcid'          :   'tc00001',
            'cache_server'  :   'localhost:56060'
            }

    callback = {
        'config'   :   'self._config_log',
        'savecms'  :   'self._report_cms',
        'snapshot' :   'self._report_snapshot',
        'log'      :   'self._report_log'
        }

    def _write_trace(self, *args):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        _title      = ''.join([_timestamp, ' '])
        _tracefile  = self.config.get('tracefile', 'cms_log.log')
        _log        = ' '.join([str(x) for x in args])
        with open (_tracefile, 'ab+') as f:
            f.write(_title)
            f.write(_log)
            f.write('\n')

    def _parse_params(self, params):
        '''
        提取请求参数
        '''
        _id     = params['id']
        _tcid   = params['tcid']
        _imei   = params.get('imei', '00000000')
        _mac    = params['mac']
        return (_id, _tcid, _imei, _mac)

    def _log_status(self, data, logtype):
        data['type']            = logtype
        data['cache_server']    = self.config['cache_server']
        data['proxy']           = dict()
        data['proxy'].update(self.config.get('proxy', {'log': '/auto/ucstart/logserver'}))
        self.plugin.do(cache_status=data)

    def _process_cms(self, request, reqid, tcid, imei, mac):
        '''
        处理客户端日志
        '''
        _data = dict()
        _data['id']     = reqid
        _data['tcid']   = tcid
        _data['imei']   = imei
        _data['mac']    = mac
        request.write(json.dumps(_data))
        return _data

    def _process_snapshot(self, request, reqid, tcid, imei, mac):
        '''
        处理客户端截屏
        '''
        _data = dict()
        _data['id']     = reqid
        _data['tcid']   = tcid
        _data['imei']   = imei
        _data['mac']    = mac
        request.write(json.dumps(_data))
        return _data

    def _process_log(self, request, reqid, tcid, imei, mac):
        '''
        处理客户端日志
        '''
        _data = dict()
        _data['id']     = reqid
        _data['tcid']   = tcid
        _data['imei']   = imei
        _data['mac']    = mac
        request.write(json.dumps(_data))
        self._log_status(_data, 'log')
        return _data

    def _process_crash(self, request, reqid, tcid, imei, mac):
        '''
        处理客户端崩溃日志
        '''
        _data = dict()
        _data['id']     = reqid
        _data['tcid']   = tcid
        _data['imei']   = imei
        _data['mac']    = mac
        request.write(json.dumps(_data))
        self._log_status(_data, 'crash')
        return _data

    def _report_cms(self, request, params, data):
        '''
        客户端上传CMS资源配置，带上ID,TCID,IMEI以及MAC
        '''
        if 'id' not in params or 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, ID/TCID/IMEI required!"
        _data = self.plugin.do(decode=data)
        self._write_trace('Received CMS Raw Data', _data)
        #_cms = json.loads(_data.replace("'", "\""))
        #self._write_trace('Received CMS', _cms)
        (_id, _tcid, _imei, _mac) = self._parse_params(params)
        return self._process_cms(request, _id, _tcid, _imei, _mac)

    def _report_snapshot(self, request, params, data):
        '''
        客户端上传首页截屏，带上ID,TCID,IMEI以及MAC
        '''
        if 'id' not in params or 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, ID/TCID/IMEI required!"
        _image  = self.plugin.do(decode=data)
        #self._write_trace('Received CMS', _cms)
        (_id, _tcid, _imei, _mac) = self._parse_params(params)
        self.plugin.do(snapshot=(_tcid, _imei, _mac, _image))
        self._write_trace('Saved Snapshot Raw Data (%s) %s_%s_%s.jpg'
                %(len(_image), _tcid, _imei, _mac))
        return self._process_snapshot(request, _id, _tcid, _imei, _mac)

    def _report_log(self, request, params, data):
        '''
        客户端上传日志，带上ID和TCID和IMEI
        '''
        if 'id' not in params or 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, ID/TCID/IMEI/MAC required!"
        _data = self.plugin.do(decode=data)
        _log = json.loads(_data.replace("'", "\""))
        self._write_trace('Received Log', _log)
        (_id, _tcid, _imei, _mac) = self._parse_params(params)
        return self._process_log(request, _id, _tcid, _imei, _mac)

    def _report_crash(self, request, params, data):
        '''
        客户端上传崩溃日志，带上ID和TCID
        '''
        if 'id' not in params or 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, ID/TCID/IMEI/MAC required!"
        (_id, _tcid, _imei, _mac) = self._parse_params(params)
        self._process_crash(request, _id, _tcid, _imei, _mac)

    def _config_log(self, request, params, data):
        '''
        配置日志服务
        '''
        _config = json.loads(data.replace("'", "\""))
        if type(_config) is dict:
            self.config = dict()
            self.config.update(_config)
            self._write_trace('Received Config', self.config)

    def _process_request(self, request, params, data):
        '''
        处理请求
        '''
        self._write_trace('Response', request.path, 'Done')
        _parts  = os.path.split(request.path)
        _action = _parts[-1]
        if _action not in self.callback:
            return 'Request not valid, no action will take!'
        self._write_trace('Received Request', request.path)
        _func = eval(self.callback[_action])
        _resp = _func(request, params, data)
        self._write_trace('Response', request.path, 'Done')
        return _resp

    def render_POST(self, request):
        '''
        监听POST请求，唯一入口
        '''
        _params = {k.lower():v[0] for k, v in request.args.items()}
        _data   = request.content.read()
        request.setResponseCode(200)
        request.setHeader('Content-Type', 'application/json; charset=UTF-8')
        self._process_request(request, _params, _data)
        request.finish()
        return server.NOT_DONE_YET
