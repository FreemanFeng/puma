# -*- coding: utf-8 -*-

import os
import json
from time import time, strftime, localtime
from datetime import datetime

from twisted.web import server, resource
from twisted.internet import reactor, endpoints, tcp

from plugin_id_cache import PluginIdCache

class IdCacheServer(resource.Resource):
    '''
    twisted api: http://twistedmatrix.com/documents/current/api/
    http://twistedmatrix.com/documents/current/api/nameIndex.html#R
    http://twistedmatrix.com/documents/current/api/twisted.web.http.Request.html
    '''
    isLeaf  = True
    plugin  = PluginIdCache()
    config  = {
            'tcid'      :   'tc00001',
            'cms'   :   'http://100.84.72.192:59090/ldus',
            #'cms'   :   'http://117.135.147.33:18080/ldus?us_ver=2.0',
            #'cms'       :   'http://117.135.147.33:18080/ldus?from=intl',
            'idm'       :   'http://10.20.35.40'
            }
    cache   = dict()
    #+================================
    #| status tuple:
    #| (Init, Log, Quit, Crash)
    #+================================
    postype = {
            'init'  :   0,
            'log'   :   1,
            'quit'  :   2,
            'crash' :   3
            }
    idstatus = {
            1 : 'cached',
            2 : 'expired',
            3 : 'timeout'
            }
    #+================================
    (WAIT_INIT, INIT_DONE, LOG_DONE, QUIT_DONE, CRASH_DONE) = (0, 1, 2, 3, 4)
    (ID_CACHED, ID_EXPIRED, ID_TIMEOUT) = (1, 2, 3)
    (ZERO_QUIT, FIRST_QUIT, SEC_QUIT, THIRD_QUIT) = (0, 1, 2, 3)

    callback = {
        'init'      :   'self._request_init',
        'tc_status' :   'self._request_tc_status',
        'id_status' :   'self._request_id_status',
        'cachelog'  :   'self._request_cachelog',
        'reset'     :   'self._request_reset',
        'expire'    :   'self._request_expire',
        'quit'      :   'self._request_quit',
        'timeout'   :   'self._request_timeout'
        }

    def _write_trace(self, *args):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        _title      = ''.join([_timestamp, ' '])
        _tracefile  = self.config.get('tracefile', 'id_cache_server.log')
        _log        = ' '.join([str(x) for x in args])
        with open (_tracefile, 'ab+') as f:
            f.write(_title)
            f.write(_log)
            f.write('\n')

    def render_POST(self, request):
        _data   = request.content.read()
        _config = json.loads(_data.replace("'", "\""))
        if type(_config) is dict:
            self.config = dict()
            self._write_trace('Received Config', _config)
            self.config.update(_config)
            self._write_trace('Saved Config', self.config)
        if 'tcid' in _config:
            _tcid = _config['tcid']
            for _key, _val in _config['mac'].items():
                _id = self.plugin.do(join=(_tcid, _key))
                self._write_trace("Config TCID MAC %s" % _id)
                self._update_tc_status(_id, 0, self.WAIT_INIT)
        request.finish()
        return server.NOT_DONE_YET

    def _update_tc_status(self, cid, pos, status):
        if cid not in self.cache:
            self.cache[cid] = [0, 0, 0, 0]
        _data = self.cache[cid]
        _data[pos] = status

    def _update_id_status(self, mid, status):
        if mid not in self.cache:
            return
        _id = self.cache[mid]
        (_id_status, _quit, _imei, _mac, _, _start) = self.cache[_id]
        _tcid = self.config['tcid']
        self.cache[_id] = (status, _quit, _imei, _mac, _tcid, _start)
        return status

    def _get_status(self, tcid, mac, pos):
        _id = self.plugin.do(join=(tcid, mac))
        if _id not in self.cache:
            self.cache[_id] = [self.WAIT_INIT, 0, 0, 0]
        self._write_trace('TCID MAC', _id, 'Status', self.cache[_id])
        _data = self.cache[_id]
        return _data[pos]

    def _parse_params(self, params):
        '''
        提取请求参数
        '''
        _id     = params['id']
        _imei   = params.get('imei', '00000000')
        _mac    = params['mac']
        return (_id, _imei, _mac)

    def _process_cached(self, request, reqid, imei, mac):
        '''
        客户端上传的ID如果已经被缓存，有两种情况:
        1. 这是在同一个测试用例里头，客户端的后续启动，带相同ID, 应答304
        2. 客户端因为崩溃，没有清理本地id文件，导致在第一次启动时，带了旧的ID, 应答4001
        '''
        (_type, _quit, _imei, _mac, _, _start) = self.cache[reqid]
        _tcid = self.config['tcid']
        _elapse = time() - _start
        _timeout = self.cache.get('timeout', 300)
        if _elapse > _timeout or _type == self.ID_EXPIRED:
            request.setResponseCode(222)
            _id = self.plugin.do(create_id=(imei, mac))
            del(self.cache[reqid])
            return self._cache_id(_id, imei, mac, _tcid, 222)
        elif _type == self.ID_CACHED:
            request.setResponseCode(333)
            return self._cache_id(reqid, imei, mac, _tcid, 333)
        elif _type == self.ID_TIMEOUT:
            request.setResponseCode(344)
            return self._cache_id(reqid, imei, mac, _tcid, 344)
        else:
            del(self.cache[reqid])
            return "Invalid Cached Status"

    def _request_id_status(self, request, params):
        '''
        设置ID状态
        '''
        if 'tcid' not in params or 'status' not in params:
            request.setResponseCode(400)
            return "Bad request, TCID/ACTION required!"
        _data   = dict()
        _tcid   = params['tcid']
        _status = int(params['status'])
        _mac    = params['mac']
        _mapid  = self.plugin.do(join=(_mac, _tcid))
        self._update_id_status(_mapid, _status)
        return json.dumps(_data)

    def _request_tc_status(self, request, params):
        '''
        获取当前测试状态
        '''
        if 'tcid' not in params or 'action' not in params:
            request.setResponseCode(400)
            return "Bad request, TCID/ACTION required!"
        _data   = dict()
        _tcid   = params['tcid']
        _action = params['action']
        _mac    = params['mac']
        _pos    = self.postype[_action]
        _data['status'] = self._get_status(_tcid, _mac, _pos)
        return json.dumps(_data)

    def _request_reset(self, request, params):
        '''
        重置测试状态
        '''
        if 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, TCID required!"
        _data   = dict()
        _tcid   = params['tcid']
        _mac    = params['mac']
        _id     = self.plugin.do(join=(_tcid, _mac))
        self.cache[_id] = [self.WAIT_INIT, 0, 0, 0]
        _data.update(params)
        _data['status'] = self.cache[_id]
        return json.dumps(_data)

    def _request_expire(self, request, params):
        '''
        设置超时时间
        '''
        _data   = dict()
        self.cache['timeout'] = int(params['expire'])
        _data['timeout'] = self.cache['timeout']
        return json.dumps(_data)

    def _request_cachelog(self, request, params):
        '''
        收到日志，设置状态为LOG_DONE
        '''
        if 'tcid' not in params:
            request.setResponseCode(400)
            return "Bad request, TCID required!"
        _data = dict()
        _tcid = params['tcid']
        _mac  = params['mac']
        _id = self.plugin.do(join=(_tcid, _mac))
        _mapid = self.plugin.do(join=(_mac, _tcid))
        self._write_trace("Update", _id, "Status to LOG DONE")
        self._update_tc_status(_id, 1, self.LOG_DONE)
        return json.dumps(params)

    def _request_timeout(self, request, params):
        '''
        客户端退出通知
        '''
        if 'timeout' not in params:
            request.setResponseCode(400)
            return "Bad request, TIMEOUT required!"
        self.cache['timeout'] = int(params['timeout'])

    def _request_quit(self, request, params):
        '''
        客户端退出通知
        '''
        if 'id' not in params:
            request.setResponseCode(400)
            return "Bad request, ID required!"
        _id = params['id']
        if _id not in self.cache:
            request.setResponseCode(400)
            return 'No ID matched for quit!'
        (_type, _quit, _imei, _mac, _tcid, _start) = self.cache[_id]
        if _quit > 0:
            _type = self.ID_EXPIRED
        self.cache[_id] = (_type, _quit + 1, _imei, _mac, _tcid, _start)
        _data = dict()
        _data['id']     = _id
        _data['tcid']   = _tcid
        _data['mac']    = _mac
        _id = self.plugin.do(join=(_tcid, _mac))
        _mapid = self.plugin.do(join=(_mac, _tcid))
        self._write_trace("Update", _id, "Status to QUIT DONE")
        self._update_tc_status(_id, 2, self.QUIT_DONE)
        return json.dumps(_data)

    def _cache_id(self, reqid, imei, mac, tcid, code = 200):
        '''
        缓存客户端ID，IMEI以及测试用例ID
        '''
        self.cache[reqid] = (self.ID_CACHED, self.ZERO_QUIT, imei, mac, tcid, time())
        _mapid = self.plugin.do(join=(mac, tcid))
        self.cache[_mapid] = reqid
        _data = dict()
        _data['id']     = reqid
        _data['tcid']   = tcid
        _data['mac']    = mac
        if 'cms' in self.config:
            _data['cms']    = self.config['cms']
        if 'idm' in self.config:
            _data['idm']    = self.config['idm']
        _data['timeout']    =   self.config.get('timeout', 20)
        _data['res']        =   self.config.get('res', ["idm"])
        _data['code']       =   code
        _id = self.plugin.do(join=(tcid, mac))
        _mapid = self.plugin.do(join=(mac, tcid))
        self._write_trace("Update", _id, "Status to INIT DONE")
        self._update_tc_status(_id, 0, self.INIT_DONE)
        return json.dumps(_data)

    def _request_init(self, request, params):
        '''
        客户端第一次启动，会发起init初始化请求，带上id, imei, mac
        '''
        if 'id' not in params or 'imei' not in params or 'mac' not in params:
            request.setResponseCode(400)
            return "Bad request, ID and IMEI and MAC required!"
        (_id, _imei, _mac) = self._parse_params(params)
        if _id in self.cache:
            return self._process_cached(request, _id, _imei, _mac)
        if 'tcid' not in self.config:
            request.setResponseCode(500)
            return "TCID not Configed!"
        return self._cache_id(_id, _imei, _mac, self.config['tcid'])

    def _process_request(self, request, params):
        '''
        处理请求
        '''
        _parts  = os.path.split(request.path)
        _action = _parts[-1]
        if _action not in self.callback:
            return 'Request not valid, no action will take!'
        self._write_trace('Received Request', request.path, 'params', params)
        _func = eval(self.callback[_action])
        _resp = _func(request, params)
        self._write_trace('Response', request.path, 'Data', _resp)
        return _resp

    def render_GET(self, request):
        '''
        GET请求入口
        '''
        _params = {k.lower():v[0] for k, v in request.args.items()}
        if 'tcid' not in self.config:
            self.config['tcid'] = 'default_tc00001'
            #request.setResponseCode(400)
            #return "TCID not Configured!"
        request.setResponseCode(200)
        request.setHeader('Content-Type', 'application/json; charset=UTF-8')
        return self._process_request(request, _params)
