# -*- coding: utf-8 -*-

import os
import json
from time import time, strftime, localtime

from twisted.web import server, resource
from twisted.internet import reactor, endpoints

class MockCmsServer(resource.Resource):
    '''
    twisted api: http://twistedmatrix.com/documents/current/api/
    http://twistedmatrix.com/documents/current/api/nameIndex.html#R
    http://twistedmatrix.com/documents/current/api/twisted.web.http.Request.html
    '''
    isLeaf  = True
    config  = dict()
    headers = dict()
    ctmap   = {
            'html'  :   'text/html; charset=UTF-8',
            'js'    :   'application/javascript; charset=UTF-8',
            'css'   :   'text/css; charset=UTF-8',
            'jpg'   :   'image/jpeg; charset=UTF-8',
            'jpeg'  :   'image/jpeg; charset=UTF-8',
            'gif'   :   'image/gif; charset=UTF-8',
            'png'   :   'image/png; charset=UTF-8',
            'bmp'   :   'image/bmp; charset=UTF-8',
            'webp'  :   'image/webp; charset=UTF-8'
            }
    imgmap  = {
            'jpg'   :   'image/jpeg; charset=UTF-8',
            'jpeg'  :   'image/jpeg; charset=UTF-8',
            'gif'   :   'image/gif; charset=UTF-8',
            'png'   :   'image/png; charset=UTF-8',
            'bmp'   :   'image/bmp; charset=UTF-8',
            'webp'  :   'image/webp; charset=UTF-8'
            }

    def render_POST(self, request):
        _data   = request.content.read()
        _config = json.loads(_data.replace("'", "\""))
        if type(_config) is dict:
            self.config.update(_config)
            print self.config
        request.finish()
        return server.NOT_DONE_YET

    def render_GET(self, request):
        if 'htdocs' not in self.config:
            request.setResponseCode(400)
            return "No Root Path configured via POST request!"
        _path = request.path
        _root = self.config['htdocs']
        _file = ''.join([_root, _path])
        if not os.path.isfile(_file):
            request.setResponseCode(404)
            return ""
        request.setResponseCode(200)
        if 'headers' in self.config:
            [request.setHeader(x, y) for x,y in self.config['headers'].items()]
        _content = str()
        with open(_file, 'rb') as f:
            _content = f.read()
            request.setHeader('Content-Length', len(_content))
        _parts  = os.path.basename(_file).split('.')
        _type   = 'html'
        if len(_parts) > 1 and _parts[-1] in self.ctmap:
            _type   = _parts[-1]
        request.setHeader('Content-Type', self.ctmap[_type])
        print "[%s] Response %s Done" % (strftime('%Y-%m-%d %H:%M:%S',localtime(time())), _path)
        return _content
