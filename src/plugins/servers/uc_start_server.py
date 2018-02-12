# -*- coding: utf-8 -*-

import os
import time
import json
from multiprocessing import Queue

from MBase import MBase
from id_cache_server import IdCacheServer
from plugin_uc_start_opt import PluginUcStartOpt
from handle_exception import handle_exception

class UcStartServer(MBase):
    '''
    运行UC启动相关的服务
    '''
    plugin = PluginUcStartOpt()
    (NOT_DONE_YET, DONE) = (0, 1)
    (OFFLINE, ONLINE) = (0, 1)
    def __init__(self, *args, **kargs):
        super(UcStartServer, self).__init__()
        self.plugin.params.clear()
        self._callback = {
                'init'  :   self._wait_init,
                'quit'  :   self._wait_quit,
                'log'   :   self._wait_log,
                'crash' :   self._wait_crash
                }

    #+===============================
    #| CMS服务相关操作
    #+===============================
    @handle_exception
    def _load_cms_template(self, platform, params):
        '''
        加载CMS模板
        '''
        _resid  = params['resid']
        _path   = params['data_path']
        return self.cms_opt(searchcms=(platform, _resid, _path))

    @handle_exception
    def _save_cms(self, path, params):
        '''
        保存CMS原始json数据
        '''
        #+=========================
        #| 1. 读取CMS资源模板
        #+=========================
        (_entid, _resid, _data) = self.cms_opt(readcms=path)
        #+=========================
        #| 2. 自动生成带默认值或空值的json数据
        #+=========================
        (_msg, _items) = self.cms_opt(load=_data)
        self.logger.info(_msg)
        #+=========================
        #| 3. 更新json数据
        #+=========================
        if 'update' in params:
            self.cms_opt(update=(_msg, params['update']))
        if 'pop' in params:
            self.cms_opt(pop=(_msg, params['pop']))
        if 'delete' in params:
            self.cms_opt(delete=(_msg, params['delete']))
        if 'append' in params:
            self.cms_opt(append=(_msg, _items, params['append']))
        if 'select' in params:
            self.cms_opt(select=(_msg, _items, params['select']))
        #+=========================
        #| 4. 保存原始json数据到CMS测试环境后台
        #+=========================
        _cond = params.get('cond', None)
        _type = params.get('data_type', 1)
        self.cms_opt(pushcms=(_resid, _msg, _cond, _type))
        self.logger.info(_msg)

    @handle_exception
    def _config_cms_service(self, platform, params):
        '''
        配置CMS服务
        '''
        #+=========================
        #| 1. 加载CMS模板
        #+=========================
        _file = self._load_cms_template(platform, params)
        self.logger.info(_file)
        #+=========================
        #| 2. 保存CMS配置的原始数据
        #+=========================
        self._save_cms(_file, params)

    #+===============================
    #| 闪屏服务相关操作
    #+===============================
    @handle_exception
    def _load_idm_template(self, platform, params):
        '''
        加载闪屏模板
        '''
        _type   = params['type']
        _path   = params['data_path']
        _name   = self.convert(join=(_type, '.json'))
        _file   = os.path.join(_path, _name)
        return self.idm_opt(readidm=_file)

    @handle_exception
    def _mock_idm(self, msg):
        '''
        配置闪屏的Mock服务
        '''
        _node   = self.cm.ucstart['mock_idm']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _path   = self.cm.proxy['mock_idm']
        _config['url'] = self.convert(join=('http://', _server, _path))
        _config['json'] = dict()
        _data = _config['json']
        _data['idm'] = dict()
        _idm = _data['idm']
        _idm.update(msg)
        self.http_opt(post_json=_config)

    @handle_exception
    def _save_idm(self, msg, params):
        '''
        更新闪屏数据
        '''
        _name = self.cm.idm['node']
        _node = self.idm_opt(get_node=(_name, msg))
        if 'update' in params:
            self.idm_opt(update=(_node, params['update']))
        if 'pop' in params:
            self.idm_opt(pop=(_node, params['pop']))
        if 'delete' in params:
            self.idm_opt(delete=(_node, params['delete']))
        if 'append' in params:
            self.idm_opt(append=(_node, params['append']))
        self._mock_idm(msg)

    @handle_exception
    def _config_idm_service(self, platform, params):
        '''
        配置闪屏服务
        '''
        #+=========================
        #| 1. 加载闪屏模板
        #+=========================
        _data = self._load_idm_template(platform, params)
        #+=========================
        #| 2. 生成闪屏的json数据
        #+=========================
        _msg = self.idm_opt(load=_data)
        #+=========================
        #| 3. 保存闪屏json数据
        #+=========================
        self._save_idm(_msg, params)

    #+===============================
    #| Cache服务相关操作
    #+===============================
    @handle_exception
    def _config_cache_service(self, params, devices):
        '''
        配置缓存服务
        '''
        _node   = self.cm.ucstart['id_cache']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _path   = self.convert(join=(self.cm.proxy['id_cache'], '/config'))
        _config['url'] = self.convert(join=('http://', _server, _path))
        _config['json'] = dict()
        _data = _config['json']
        _data.update(params)
        _data['mac'] = dict()
        _mac = _data['mac']
        for _serial, _val in devices.items():
            _key = _val['mac']
            _mac[_key] = _serial
        self.logger.info('Config Cache Params:%s, MAC:%s' % (params, _mac))
        self.http_opt(post_json=_config)

    @handle_exception
    def _get_tc_status(self, params, mac, serial, action):
        '''
        从ID Cache缓存中获取TCID及状态
        '''
        _node   = self.cm.ucstart['id_cache']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _tcid   = params['tcid']
        _path   = self.convert(join=(self.cm.proxy['id_cache'], '/tc_status'))
        _url    = self.convert(join=('http://', _server, _path))
        _params = self.convert(params=('mac', mac, 'serial', serial,
                               'tcid', _tcid, 'action', action))
        _config['url'] = self.convert(join=(_url, '?', _params))
        self.http_opt(request=_config)
        _content = self.http_opt(get_content=1)
        self.logger.info(_content)
        return _content

    @handle_exception
    def _update_id_status(self, params, status):
        '''
        设置ID状态
        '''
        _cache  = params['id_cache']
        _mac    = params['mac']
        _node   = self.cm.ucstart['id_cache']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _tcid   = _cache['tcid']
        _path   = self.convert(join=(self.cm.proxy['id_cache'], '/id_status'))
        _url    = self.convert(join=('http://', _server, _path))
        _params = self.convert(params=('mac', _mac, 'tcid', _tcid, 'status', status))
        _config['url'] = self.convert(join=(_url, '?', _params))
        self.http_opt(request=_config)
        _content = self.http_opt(get_content=1)
        self.logger.info(_content)
        return _content

    @handle_exception
    def _reset_status(self, params, mac):
        '''
        重置测试用例状态
        '''
        _node   = self.cm.ucstart['id_cache']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _tcid   = params['tcid']
        _path   = self.convert(join=(self.cm.proxy['id_cache'], '/reset'))
        _url    = self.convert(join=('http://', _server, _path))
        _params = self.convert(params=('mac', mac, 'tcid', _tcid))
        _config['url'] = self.convert(join=(_url, '?', _params))
        self.http_opt(request=_config)
        _content = self.http_opt(get_content=1)
        self.logger.info(_content)
        return _content

    @handle_exception
    def _set_expire_time(self, params):
        '''
        设置ID过期
        '''
        _node   = self.cm.ucstart['id_cache']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _expire = params.get('expire', 300)
        _path   = self.convert(join=(self.cm.proxy['id_cache'], '/expire'))
        _url    = self.convert(join=('http://', _server, _path))
        _path   = self.convert(join=('?expire=', _expire))
        _config['url'] = self.convert(join=(_url, _path))
        self.http_opt(request=_config)
        _content = self.http_opt(get_content=1)
        self.logger.info(_content)
        return _content

    #+===============================
    #| Log服务相关操作
    #+===============================
    @handle_exception
    def _config_log_service(self, params):
        '''
        配置缓存服务
        '''
        _node   = self.cm.ucstart['log']
        _server = self.convert(join=(_node['server'], ':', _node['port']))
        _config = dict()
        _path   = self.convert(join=(self.cm.proxy['log'], '/config'))
        _config['url'] = self.convert(join=('http://', _server, _path))
        _config['json'] = dict()
        _data = _config['json']
        _data['proxy'] = dict()
        _data.update(params)
        _data['proxy'].update(self.cm.proxy)
        self.http_opt(post_json=_config)

    #+===============================
    #| 配置服务入口
    #+===============================
    @handle_exception
    def _config_services(self, params):
        '''
        配置CMS/IDM/ID CACHE服务
        '''
        _platform = params['platform']
        if 'cms' in params:
            self._config_cms_service(_platform, params['cms'])
        if 'idm' in params:
            self._config_idm_service(_platform, params['idm'])
        self._config_cache_service(params['id_cache'], params['devices'])
        self._config_log_service(params['log'])
        time.sleep(self.cm.cms_wait)

    #+===============================
    #| 执行测试入口
    #+===============================
    @handle_exception
    def _wait_status(self, action, params, status):
        _resp = self._get_tc_status(params['id_cache'], params['mac'],
                                    params['serial'], action)
        _data = json.loads(_resp)
        if _data['status'] == status:
            return self.DONE
        return self.NOT_DONE_YET

    @handle_exception
    def _wait_init(self, action, params):
        return self._wait_status(action, params, IdCacheServer.INIT_DONE)

    @handle_exception
    def _wait_quit(self, action, params):
        return self._wait_status(action, params, IdCacheServer.QUIT_DONE)

    @handle_exception
    def _wait_log(self, action, params):
        return self._wait_status(action, params, IdCacheServer.LOG_DONE)

    @handle_exception
    def _wait_crash(self, action, params):
        return self._wait_status(action, params, IdCacheServer.CRASH_DONE)

    @handle_exception
    def _wait_ready(self, action, params, timeout = None):
        if timeout is None:
            timeout = int(params['timeout'][action])
        if timeout < 0:
            return self.NOT_DONE_YET
        time.sleep(1.0)
        if self._callback[action](action, params) == self.NOT_DONE_YET:
            return self._wait_ready(action, params, timeout - 1)
        return self.DONE

    @handle_exception
    def _start(self, params):
        '''
        启动UC前，需先重置测试状态以及退出UC
        '''
        #+=========================
        #| 重置测试状态
        #+=========================
        self._reset_status(params['id_cache'], params['mac'])
        #+=========================
        #| 执行前，确保UC已退出
        #+=========================
        self.app_opt(stop=params)
        #+=========================
        #| 启动UC
        #+=========================
        self.app_opt(start=params)

    @handle_exception
    def _last_restart(self, params, queue, message):
        '''
        超时后，重新启动一次UC，获取日志
        '''
        #+=========================
        #| 设置ID超时
        #+=========================
        self._update_id_status(params, IdCacheServer.ID_TIMEOUT)
        #+=========================
        #| 启动UC
        #+=========================
        self._start(params)
        #+=========================
        #| 有可能UC不上传日志
        #+=========================
        self._wait_ready('log', params)
        _id = self.plugin.do(join=(params['imei'], params['mac']))
        _log = self.convert(join=(_id, '->', message))
        queue.put({params['serial']: _log})

    @handle_exception
    def _execute(self, data, *args, **kargs):
        '''
        执行测试
        '''
        (params, queue) = data
        #+=========================
        #| 保存进程id到文件，用于清理现场
        #+=========================
        self.queue_opt(store_pid=(os.getpid(), params))
        #+=========================
        #| 设置缓存过期时间
        #+=========================
        self._set_expire_time(params['timeout'])
        #+=========================
        #| 启动UC
        #+=========================
        self._start(params)
        #+=========================
        #| 等待初始化请求
        #+=========================
        if self._wait_ready('init', params) != self.DONE:
            return self._last_restart(params, queue, '1st Init Failed')
        #+=========================
        #| 等待UC退出
        #+=========================
        if self._wait_ready('quit', params) != self.DONE:
            return self._last_restart(params, queue, '1st Quit Failed')
        #+=========================
        #| 启动UC
        #+=========================
        self._start(params)
        #+=========================
        #| 等待初始化请求
        #+=========================
        if self._wait_ready('init', params) != self.DONE:
            return self._last_restart(params, queue, '2nd Init Failed')
        #+=========================
        #| 等待日志上传
        #+=========================
        if self._wait_ready('log', params) != self.DONE:
            return self._last_restart(params, queue, '2nd Log Failed')
        #+=========================
        #| 设置ID过期
        #+=========================
        self._update_id_status(params, IdCacheServer.ID_EXPIRED)
        #+=========================
        #| 通知完成
        #+=========================
        return queue.put((params['serial'], params['mac'], params['imei']))

    @handle_exception
    def _post_condition(self, params, queue):
        '''
        清理现场
        '''
        _fails  = list()
        _all    = list()
        for _item in params['devices']:
            _ret = queue.get()
            if type(_ret) is dict:
                _fails.append(_ret)
            _all.append(_ret)
        self.queue_opt(clear_pids=params)
        assert len(_fails) == 0, str(_fails)
        self.logger.info('All Phone %s passed testing' % _all)

    @handle_exception
    def _is_online(self, params, serial):
        '''
        检测手机是否Online
        '''
        _debug  = params.get('debug_device', '1')
        if int(_debug) != 1:
            #+=========================
            #| Hive手机
            #+=========================
            _conn   = self.hive_opt(get_connect=serial)
            if 'remoteConnectUrl' not in _conn:
                self.logger.info('Device %s not online' % serial)
                return self.OFFLINE
        return self.ONLINE

    @handle_exception
    def _execute_testing(self, params):
        '''
        执行测试
        '''
        _queue = Queue()
        _black_list = list()
        for _serial, _val in params['devices'].items():
            #+=========================
            #| 确认Hive手机在线或是本地手机
            #+=========================
            if self._is_online(params, _serial) == self.OFFLINE:
                _black_list.append(_serial)
                continue
            _params = dict()
            _params.update(params)
            _platform = _params['platform']
            _node = _params[_platform]
            _node.update(_val)
            _params.update(_val)
            _params['serial'] = _serial
            #self._execute((_params, _queue))
            self.start_proc(0, self._execute, _queue, _params, _queue)
        _devices = params['devices']
        #+=========================
        #| 剔除不在线Hive手机
        #+=========================
        for _serial in _black_list:
            del(_devices[_serial])
        #+=========================
        #| 清理进程，检查执行结果
        #+=========================
        self._post_condition(params, _queue)

    @handle_exception
    def run(self, queue=None, *args, **kargs):
        '''
        唯一入口，运行跟UC启动相关的测试服务
        '''
        #+=========================
        #| 初始化单例
        #+=========================
        self.plugin.do(start=1)
        #+=========================
        #| 配置各种服务
        #+=========================
        self._config_services(self.plugin.params)
        #+=========================
        #| 执行测试服务
        #+=========================
        self._execute_testing(self.plugin.params)
        #+=========================
        #| 结束，清理单例的数据
        #+=========================
        self.plugin.params.clear()
