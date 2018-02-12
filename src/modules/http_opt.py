# -*- coding:utf-8 -*-
'''
This Class is to send http request
'''
import re
import traceback

import httplib2
import requests

from binding import Binding
from SBase import SBase
from handle_exception import handle_exception

class HttpOpt(SBase):
    '''
    Class for Db Operation
    '''
    def __init__(self, *args, **kargs):
        '''
        Call db opt by default
        '''
        super(HttpOpt, self).__init__()
        self.http       = None
        self.response   = None
        self.content    = None


    @handle_exception
    def http_opt(self, *args, **kargs):
        '''
        unique interface for http operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _get_response(self, *args, **kargs):
        return self.response

    @handle_exception
    def _get_content(self, *args, **kargs):
        return self.content

    @handle_exception
    def _build_request(self, config, *args, **kargs):
        '''
        build request data
        '''
        _method     = config.get('method', 'POST')
        _url        = config.get('url', '/')
        _headers    = config.get('headers', dict())
        _body       = config.get('body', str())
        _req        = ['%s %s HTTP/1.0\r\n' % (_method, _url)]
        for _key, _value in _headers.items():
            _req.append(self.convert(join=(_key, ': ', _value, '\r\n')))
        _req.append('\r\n')
        _req.append(_body)
        return self.convert(join=_req)

    @handle_exception
    def _request(self, config, *args, **kargs):
        '''
        send HTTP Request
        '''
        url     = config['url']
        method  = config.get('method', 'GET')
        body    = config.get('body', None)
        headers = config.get('headers', None)
        self.convert(dict_to_str=headers)
        self.http = httplib2.Http(timeout=180)
        try:
            (_response, _content)=self.http.request(url, method, body, headers)
            self.response = _response
            self.content  = _content
        except:
            self.logger.info(traceback.format_exc())
            return

        self.logger.info("%s %s [%s]" % (method, url, self.response.status))
        return self.response.status

    @handle_exception
    def _post_data(self, config, *args, **kargs):
        '''
        send HTTP Request
        '''
        _url        = config['url']
        _data       = config['data']
        _headers    = config.get('headers', None)
        _req    = requests.post(_url, data = _data, headers = _headers)
        self.logger.info("POST %s [%s]" % (_url, _req.status_code))
        return _req.status_code

    @handle_exception
    def _post_json(self, config, *args, **kargs):
        '''
        send HTTP Request
        '''
        _url        = config['url']
        _data       = config['json']
        _headers    = config.get('headers', None)
        _req        = requests.post(_url, json = _data, headers = _headers)
        self.logger.info("POST JSON %s [%s]" % (_url, _req.status_code))
        return _req.status_code

    @handle_exception
    def post_file(self, config, **kargs):
        '''
        send HTTP Request
        '''
        _url        = config['url']
        _path       = self.absolute_path(config['file'])
        _ct         = config.get('content_type', None)
        _headers    = config.get('headers', None)
        _files      = dict()
        if _ct is None:
            _files['file'] = (config['name'], open(_path, 'rb'))
        elif _headers is None:
            _files['file'] = (config['name'], open(_path, 'rb'), _ct)
        else:
            _files['file'] = (config['name'], open(_path, 'rb'), _ct, _headers)

        _req = requests.post(_url, files=_files, **kargs)

        self.logger.info("POST %s [%s]" % (_url, _req.status_code))
        return _req

    @handle_exception
    def get_url(self, config, **kargs):
        '''
        send HTTP Request
        '''
        _url        = config['url']
        _params     = config.get('params', None)
        _headers    = config.get('headers', None)
        _timeout    = config.get('timeout', 20)
        _proxies    = config.get('proxies', None)
        _req = requests.get(_url, params=_params, headers=_headers,
                timeout=_timeout, proxies=_proxies, **kargs)

        self.logger.info("GET %s [%s]" % (_url, _req.status_code))
        #self.logger.info("GET %s Response Content [%s]" % (_url, _req.text))
        return _req
