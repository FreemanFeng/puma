# -*- coding: utf-8 -*-

import os
import json
from time import time, strftime, localtime
from datetime import datetime

from plugin_idm import PluginIdm
from twisted.web import server, resource
from twisted.internet import reactor, endpoints, tcp

class MockIdmServer(resource.Resource):
    '''
    twisted api: http://twistedmatrix.com/documents/current/api/
    http://twistedmatrix.com/documents/current/api/nameIndex.html#R
    http://twistedmatrix.com/documents/current/api/twisted.web.http.Request.html
    '''
    isLeaf  = True
    config  = dict()
    plugin  = PluginIdm()

    def _write_trace(self, *args):
        _timestamp  = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        _title      = ''.join([_timestamp, ' '])
        _tracefile  = self.config.get('tracefile', 'mock_idm_server.log')
        _log        = ' '.join([str(x) for x in args])
        with open (_tracefile, 'ab+') as f:
            f.write(_title)
            f.write(_log)
            f.write('\n')

    def _process_request(self, request):
        _params = {k.lower():v[0] for k, v in request.args.items()}
        if 'id' not in _params or 'tcid' not in _params:
            request.setResponseCode(400)
            return "Bad request, ID and TC required!"
        _id     = _params['id']
        _tcid   = _params['tcid']
        self._write_trace('Received Request', request.path, 'params', _params)
        request.setResponseCode(200)
        request.setHeader('Content-Type', 'application/json; charset=UTF-8')
        _data = self.config.get('idm', None)
        if _data is None:
            _path = 'testing/ucstart/data/idm/video.json'
            return self.plugin.idm_opt(readidm=_path)
        _resp = json.dumps(_data)
        self._write_trace('Response', request.path, 'Data', _resp)
        return _resp

    def render_POST(self, request):
        _data   = request.content.read()
        _path   = os.path.basename(request.path)
        if _path == 'getidm':
            _response = self._process_request(request)
            request.write(_response)
            request.finish()
            return server.NOT_DONE_YET
        _config = json.loads(_data.replace("'", "\""))
        if type(_config) is dict:
            self.config = dict()
            self.config.update(_config)
            self._write_trace('Received Config', self.config)
        request.finish()
        return server.NOT_DONE_YET

    def render_GET(self, request):
        return self._process_request(request)
