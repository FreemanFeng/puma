# -*- coding:utf-8 -*-

import os
import re
import time
from urllib import quote

from SBase import SBase
from binding import Binding
from handle_exception import handle_exception

class RobotOpt(SBase):
    def __init__(self, *args, **kargs):
        super(RobotOpt, self).__init__()
        self.global_config = dict()
        self.global_result = dict()
        _modules = {
                'local_port'    :   'LocalPort',
                'remote_port'   :   'RemotePort',
                'app_opt'       :   'AppOpt',
                'hive_opt'      :   'HiveOpt'
                }
        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def robot_opt(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    #===================================================================
    # utility with return value
    #===================================================================
    def _url_encode(self, url, *args, **kargs):
        return quote(url)

    def _dict_value(self, config, *args, **kargs):
        (data, key) = config
        return data.get(key, None)

    def _store_dict(self, data, key, value, *args, **kargs):
        if type(value) is dict:
            data[key] = dict()
            data[key].update(value)
        else:
            data[key] = value

    def _cache_result(self, data, *args, **kargs):
        (key, value, ret_type) = data
        if ret_type is None:
            self._store_dict(self.global_result, key, value)
        else:
            if ret_type not in self.global_result:
                self.global_result[ret_type] = dict()
            _ret = self.global_result[ret_type]
            self._store_dict(_ret, key, value)
        return value

    def _init_cache(self, *args, **kargs):
        self.global_result      = dict()
        self.cm.cp_once         = dict()
        self.cm.preconf_once    = list()
        self.cm.steps_once      = list()

    def _get_cache(self, data, *args, **kargs):
        (key, ret_type) = data
        if ret_type is None:
            return self.global_result.get(key, None)
        else:
            _ret = self.global_result.get(ret_type, None)
            if key is None:
                return _ret
            if _ret:
                return _ret.get(key, None)

    def _save_pids_queue(self, data, *args, **kargs):
        (name, pids_queue) = data
        _ret = self.robot_opt(get_cache=('pids_queue', None))
        if not _ret:
            _ret = dict()
        _ret[name] = pids_queue
        self.robot_opt(cache_result=('pids_queue', _ret, None))

    def _clear_pids_queue(self, name, *args, **kargs):
        _ret = self.robot_opt(get_cache=('pids_queue', None))
        if not _ret:
            return
        _pids_queue = _ret.get(name, None)
        if _pids_queue:
            del _ret[name]
        self.robot_opt(cache_result=('pids_queue', _ret, None))

    def _init_upload(self, *args, **kargs):
        _project    = self.cm.global_config['project']
        _path       = self.convert(join=(_project, '/data/upload'))
        _upload     = self.absolute_path(_path)
        self._update_params(['data_upload', _upload])
        return _upload

    def _upload_path(self, *args, **kargs):
        _upload = self.robot_opt(get_param=('data_upload', None))
        if _upload is None:
            return self._init_upload()
        return _upload

    def _init_data(self, folder, *args, **kargs):
        _project    = self.cm.global_config['project']
        _path       = self.convert(join=(_project, '/data/', folder))
        return self.absolute_path(_path)

    def _init_path(self, path, *args, **kargs):
        return self.absolute_path(path)

    def _init_output(self, format, *args, **kargs):
        _project    = self.cm.global_config['project']
        _path       = self.convert(join=(_project, '/data/output'))
        _out        = self.absolute_path(_path)
        self._update_params(['data_output', _out])
        self._update_params(['output_format', format])
        return self.robot_opt(local_path=(_path, format))

    def _init_pids_output(self, *args, **kargs):
        _project    = self.cm.global_config['project']
        _path       = self.convert(join=(_project, '/data/pids'))
        _out        = self.absolute_path(_path)
        self.cm.global_config['pids_output'] = _out
        self._update_params(['pids_output', _out])
        return _out

    def _output_path(self, *args, **kargs):
        _output = self.robot_opt(get_param=('data_output', None))
        if _output is None:
            return self._init_output('data')
        return _output

    def _pids_path(self, *args, **kargs):
        _output = self.robot_opt(get_param=('pids_output', None))
        if _output is None:
            return self._init_pids_output()
        return _output

    def _update_path_params(self, path, *args, **kargs):
        _name = os.path.basename(path)
        self._update_params(['image_path', path])
        self._update_params(['image_name', _name])
        return path

    def _locate_image(self, data, *args, **kargs):
        (name, pos) = data
        if pos is None:
            return name
        _project    = self.cm.global_config['project']
        _path       = self.convert(join=(_project, '/data/images/', pos, '/'))
        _file       = self.convert(join=(_path, name))
        return self.absolute_path(_file)

    #===================================================================
    # html related
    #===================================================================
    def _html_subres(self, data, *args, **kargs):
        (maindoc, url) = data
        _subres = self.html_opt(parse_subres=maindoc)
        return self.html_opt(convert_subres=(url, _subres))

    def _outlink_subres(self, data, *args, **kargs):
        _subres = self.robot_opt(html_subres=data)
        return [x[0] for x in _subres]

    def _origin_subres(self, data, *args, **kargs):
        _subres = self.robot_opt(html_subres=data)
        return [x[1] for x in _subres]

    def _converted_subres(self, data, *args, **kargs):
        _subres = self.robot_opt(html_subres=data)
        return [x[2] for x in _subres]

    #===================================================================
    # config related
    #===================================================================
    def _load_config(self, path, *args, **kargs):
        self.logger.info('Loading Config %s' % path)
        if self.cm.global_config is not None:
            #self.logger.info('Config Global %s' % self.cm.global_config)
            self.global_config.update(self.cm.global_config)
        _config = self.absolute_path(path)
        self.load_extra_config(_config)
        self.global_config['load_config'] = _config

    def _init_global_config(self, *args, **kargs):
        self.cm.global_config = dict()
        _global = self.cm.global_config
        _global['servers'] = dict()

    def _init_project(self, name, *args, **kargs):
        if self.cm.global_config is None:
            self._init_global_config()
        _htdocs = self.convert(join=(name, '/data/htdocs'))
        self.cm.global_config['project']    = name
        self.cm.global_config['htdocs']     = self.absolute_path(_htdocs)
        self.cm.global_config['bin']        = self.absolute_path('bin')
        self._update_global()
        self.robot_opt(init_output='out')
        self.robot_opt(init_pids_output=1)

    def _apply_devices(self, data, *args, **kargs):
        if self.cm.global_config is None:
            self._init_global_config()
        (count, params) = data
        self.logger.info(data)
        self.cm.global_config['devices'] = dict()
        _devices = self.cm.global_config['devices']
        if int(params['debug_device']) == 1:
            _serial = params['device_name']
            _devices[_serial] = {
                    'device_name'   :   _serial,
                    'imei'          :   params['imei'],
                    'mac'           :   params['mac']
                    }
            return
        _devices.update(self.hive_opt(apply_devices=data))

    def _install_app(self, data, *args, **kargs):
        (count, params) = data
        _params = dict()
        _params.update(self.cm.global_config)
        _params.update(params)
        _platform = params['platform']
        _params[_platform] = dict()
        _params[_platform].update(params)
        _params['devices'] = dict()
        _params['devices'].update(self.cm.global_config['devices'])
        #self.logger.info(_params)
        return self.app_opt(multi_install=_params)

    def _init_devices(self, *args, **kargs):
        _devices = self.cm.global_config['devices']
        self.robot_opt(update_params=('devices', _devices))

    def _return_devices(self, *args, **kargs):
        self.hive_opt(return_devices=1)

    def _update_global(self):
        if self.global_config is not None:
            self.cm.global_config.update(self.global_config)

    def _init_bench(self, script, *args, **kargs):
        _project    = self.cm.global_config['project']
        _bench      = self.convert(join=(_project, '/benchmark/scripts/'))
        _script     = self.convert(join=(_bench, script))
        self.cm.global_config['script']     = self.absolute_path(_script)
        self.cm.global_config['bench']      = self.absolute_path(_bench)
        self._update_global()

    def _ports_range(self, data, *args, **kargs):
        (name, min_port, max_port) = data
        _min = self.convert(join=(name, '_min_port'))
        _max = self.convert(join=(name, '_max_port'))
        self.cm.global_config[_min] = min_port
        self.cm.global_config[_max] = max_port

    #===================================================================
    # overide default config in ../../etc/apps/image_cloud/ic_config.yml
    #===================================================================
    def _random_remote_port(self, config, *args, **kargs):
        (host, name) = config
        _min = self.cm.global_config.get('remote_min_port', 10000)
        _max = self.cm.global_config.get('remote_max_port', 60000)
        return self.remote_port(get=(host, name, 1, _min, _max))

    def _set_server(self, data, *args, **kargs):
        (name, host, port) = data
        if self.cm.global_config is None:
            self._init_global_config()
        _config = self.cm.global_config['servers']
        if name not in _config:
            _config[name] = dict()
        _server = _config[name]
        _server['server'] = host
        if port is None:
            _server['port'] = self.robot_opt(random_remote_port=(host, name))
        else:
            _server['port'] = int(port)
        self.robot_opt(ssh_default=name)
        self.logger.info('Set Server %s:%s' % (host, _server['port']))

    def _ssh_default(self, name, *args, **kargs):
        self.cm.global_config['default_server'] = name
        self.logger.info('Set SSH Default to %s' % name)

    def _default_server(self, *args, **kargs):
        return self.cm.global_config['default_server']

    def _server_ssh_config(self, data, *args, **kargs):
        (name, key) = data
        assert 'servers' in self.cm.global_config, "Server %s Not Configured" % name
        _config = self.cm.global_config['servers']
        _server = _config[name]
        self.logger.info('Server %s %s = %s' % (name, key, _server[key]))
        return _server[key]

    def _server_port(self, name, *args, **kargs):
        return self.robot_opt(server_ssh_config=(name, 'port'))

    def _server_host(self, name, *args, **kargs):
        return self.robot_opt(server_ssh_config=(name, 'server'))

    def _is_alive(self, *args, **kargs):
        name  = self._default_server()
        _host = self._server_host(name)
        _port = self._server_port(name)
        return self.remote_port(is_occupied=(_host, _port))

    def _wait_alive(self, *args, **kargs):
        for x in range(10):
            if self._is_alive():
                return
            self.logger.info('sleeping 0.2s for server alive ...')
            time.sleep(0.2)
        assert 0 == 1, '[FATAL ERROR] Server not Alive!'

    def _keep_alive(self, *args, **kargs):
        name  = self._default_server()
        if not self._is_alive():
            self._stop_server(name)
            time.sleep(1)
            self._start_server((name, 1.0))
            time.sleep(1)

    def _init_servers(self, servers_config, *args, **kargs):
        if self.cm.global_config is None:
            self._init_global_config()
        _config = self.cm.global_config['servers']
        if _config:
            servers_config.update(_config)

    def _set_variable(self, data, *args, **kargs):
        (name, value) = data

    def _add_callback(self, entity, keyword, params, config):
        _func_name = keyword.replace(' ', '_')
        _name = _func_name.lower()
        if getattr(entity, _name, None) is None:
            _name = self.convert(join=('caller.', _name))
        _args = str()
        if params:
            _args = [self.convert(join=('"', x, '"')) for x in params]
            _args = self.convert(args=_args)
        _callback = self.convert(join=(_name, '(', _args, ')'))
        config.append(_callback)

    def _pre_config(self, data, *args, **kargs):
        (entity, keyword, params) = data
        if self.cm.preconf_once is None:
            self.cm.preconf_once = list()
        self._add_callback(entity, keyword, params, self.cm.preconf_once)

    def _to(self, data, *args, **kargs):
        (entity, keyword, params) = data
        if self.cm.steps_once is None:
            self.cm.steps_once = list()
        self._add_callback(entity, keyword, params, self.cm.steps_once)
        #self.cm.steps_once.reverse()

    def _local_path(self, data, *args, **kargs):
        (path, postfix) = data
        _name = self.convert(sign=8)
        _name = self.convert(join=(_name, '.', postfix))
        _path = self.absolute_path(path)
        return os.path.join(_path, _name)


    def _config_param(self, data, *args, **kargs):
        (key, value) = data
        self.cm.params[key] = value

    def _config_params(self, config, *args, **kargs):
        self.cm.params.update(config)

    @handle_exception
    def _pre_condition(self, entity, *args, **kargs):
        self.cm.preconf.extend(self.cm.preconf_once)
        _configs = [self.convert(join=('entity.', x)) for x in self.cm.preconf]
        [eval(x) for x in _configs]
        self.cm.preconf_once = None

    @handle_exception
    def _set_timeout(self, timeout, *args, **kargs):
        self.cm.timeout = timeout

    @handle_exception
    def _run_steps(self, entity, *args, **kargs):
        self.cm.steps.extend(self.cm.steps_once)
        _steps = [self.convert(join=('entity.', x)) for x in self.cm.steps]
        [eval(x) for x in _steps]
        self.cm.steps_once = None

    def _check_point(self, data, *args, **kargs):
        (cp_type, key, opcode, value, extra_key) = data
        if self.cm.cp_once is None:
            self.cm.cp_once = dict()
        if cp_type not in self.cm.cp_once:
            self.cm.cp_once[cp_type] = dict()
        _cp_type = self.cm.cp_once[cp_type]
        _cp_type[key] = dict()
        _cp = _cp_type[key]
        _cp['opcode']       = opcode
        _cp['value']        = value
        _cp['extra_key']    = extra_key
        self.logger.info("check point [%s] key[%s] %s value[%s] extra key[%s]"
                % (cp_type, key, opcode, value, extra_key))

    def _init_params(self, *args, **kargs):
        self.cm.params  = dict()
        self.cm.results = dict()
        self.cm.cp      = dict()
        self.cm.steps   = list()
        self.cm.preconf = list()
        self.cm.mode    = 'robot'
        _cache = self._get_cache(('cache', None))
        if _cache is not None and type(_cache) is dict:
            [self._update_params([x, y]) for x,y in _cache.items()]

    def _show_result(self, ret_type, data):
        for _key, _val in data.items():
            self.logger.info("[%s] key[%s] value[%s]" % (ret_type, _key, _val))

    def _get_result(self, data, *args, **kargs):
        (ret_type, key) = data
        ret = self.cm.results.get(ret_type, None)
        if key is None or ret is None or key not in ret:
            return ret
        return ret[key]

    def _show_results(self, *args, **kargs):
        self.logger.info('Reading Result ...')
        for _type, _data in self.cm.results.items():
            self._show_result(_type, _data)

    def _wrap_check(self, data, *args, **kargs):
        (key, result, opcode, value) = data
        _expected = dict()
        _expected['opcode']     = opcode
        _expected['value']      = value
        _ret        = dict()
        _ret[key]   = result
        #assert self._check(key, _ret, _expected), "[FATAL ERROR] Expected key[%s] %s value[%s], but do not satisfied " % (key, _expected['opcode'], _expected['value'])
        assert self._check(key, _ret, _expected), "[FATAL ERROR] Expected key[%s] %s value[%s], Got Result: %s \n%s" % (key, _expected['opcode'], _expected['value'], _ret, self._show_results())

    def _check(self, key, result, expected):
        _opcode = expected['opcode'].lower()
        _value  = expected['value']
        _extra  = expected.get('extra_key', None)
        if _extra is not None:
            result = result.get(_extra, None)
            assert result is not None, "[FATAL ERROR] extra key[%s] not in result[%s]" % (_extra, result)
        if _opcode == 'not':
            self.logger.info("Checking if key[%s] not in result[%s] ..." % (key, result))
            assert key not in result, "[FATAL ERROR] key[%s] expected to be not precent in result[%s]" % (key, result)
            return True
        else:
            assert key in result, "[FATAL ERROR] key[%s] type[%s] expected to be precent in result[%s]" % (key, type(key), result)
        self.logger.info("Checking if key[%s] result[%s] %s expected[%s] ..." % (key, result[key], _opcode, _value))
        if _opcode == 'exists':
            return (key in result)
        _result = str(result[key])
        if _opcode == '=':
            if type(_value) in (int, float):
                return (float(_result) == _value)
            return (_result == _value)
        elif _opcode == '!=':
            if type(_value) in (int, float):
                return (float(_result) != _value)
            return (_result != _value)
        elif _opcode == '<':
            return (float(_result) < float(_value))
        elif _opcode == '>':
            return (float(_result) > float(_value))
        elif _opcode == 'has':
            return (len(_result.split(_value)) > 1)
        elif _opcode == 'in':
            return (len(_value.split(_result)) > 1)
        elif _opcode == 'without':
            return (len(_result.split(_value)) == 1)
        elif _opcode == 'time_match':
            return ((int(_result) - 3 <= int(_value)) and (int(_value) <= int(_result) + 3))
        elif _opcode == 'match':
            if type(_value) in (int, float):
                return (float(_result) == _value)
            return (_result == _value)

        self.logger.info('[FATAL ERROR] UNKNOWN OPCODE')

    def _check_if_ok(self, *args, **kargs):
        if self.cm.cp_once:
            self.cm.cp.update(self.cm.cp_once)
            self.cm.cp_once = None
        for _type, _data in self.cm.cp.items():
            _result = self.cm.results.get(_type, None)
            assert _result is not None, "[FATAL ERROR] [%s] NO RESULT" % _type
            for _key, _val in _data.items():
                assert self._check(_key.encode('utf-8'), _result, _val), \
                        "[FATAL ERROR] Expected [%s] key[%s] %s value[%s], Got Result: %s\n%s" \
                        % (_type, _key, _val['opcode'], _val['value'], _result, self._show_results())
        if 'cache' in self.cm.results:
            self._cache_result(('cache', self.cm.results['cache'], None))

    def _to_utf8(self, params, *args, **kargs):
        return [x.encode('utf-8') for x in params]

    def _to_dict(self, params, *args, **kargs):
        _keys = params[0::2]
        _vals = params[1::2]
        return {_keys[x]:_vals[x] for x in range(len(_keys))}

    def _config_test(self, params, *args, **kargs):
        self.cm.params_once = self._to_dict(params)

    def _update_params(self, params, *args, **kargs):
        if self.cm.params_once is None:
            self.cm.params_once = self._to_dict(params)
        else:
            self.cm.params_once.update(self._to_dict(params))

    def _get_param(self, data, *args, **kargs):
        (key, default) = data
        if self.cm.params_once is not None:
            return self.cm.params_once.get(key, default)
        return default

    def _update_dict_param(self, data, *args, **kargs):
        (name, value) = data
        if self.cm.params_once is None:
            self.cm.params_once = dict()
        if name not in self.cm.params_once:
            self.cm.params_once[name] = dict()
        _field = self.cm.params_once[name]
        if value and type(value) is dict:
            _field.update(value)
        #assert 1==0, "params:%s" % self.cm.params_once

    def _clear_params(self, *args, **kargs):
        self.cm.params_once = None

    def _random_local_port(self, config, *args, **kargs):
        (name, cnt) = config
        _min = self.cm.global_config.get('local_min_port', 10000)
        _max = self.cm.global_config.get('local_max_port', 60000)
        return self.local_port(get=(name, cnt, _min, _max))

    def _extra_server(self, data, *args, **kargs):
        (name, proto, port, timeout) = data
        if self.cm.server is None:
            self.cm.server = list()
        _cnt = len(self.cm.server)
        _server = dict()
        if port:
            _server['port'] = int(port)
        else:
            _server['port'] = self.robot_opt(random_local_port=(name, _cnt))

        _server['proto']    = proto
        _server['timeout']  = timeout
        _server['name']     = name
        _server['cnt']      = _cnt
        self.cm.server.insert(0, _server)
        #self.cm.server.append(_server)
        #self.cm.server.reverse()
        return _server['port']

    #===================================================================
    # server related
    #===================================================================
    def _path(self, root, path):
        if path.startswith('/') or path.startswith('.'):
            return path
        return os.path.join(root, path)

    def _create_path(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def _server_config(self, name, *args, **kargs):
        assert 'server_configs' in self.cm.global_config
        _configs        = self.cm.global_config['server_configs']
        _hosts          = self.cm.global_config['hosts']
        _config         = _configs[name]
        _ret            = dict()
        _user           = _config['user']
        _path           = _config['path']
        _home           = os.path.join('/home', _user)
        _root           = _config.get('root', _home)
        _ret['root']    = os.path.join(_root, _path)
        _ret['start']   = self._path(_ret['root'], _config['start'])
        _ret['stop']    = self._path(_ret['root'], _config['stop'])
        _ret['core']    = self._path(_ret['root'], _config['core'])
        _ret['logs']    = self._path(_ret['root'], _config.get('logs', ''))
        _ret['elogs']   = self._path(_ret['root'], _config.get('elogs', ''))
        _ret['etc']     = self._path(_ret['root'], _config.get('etc', ''))
        _ret['extra']   = self._path(_ret['root'], _config.get('extra', ''))
        _ret['user']    = _user
        return _ret

    def _config_server(self, data, *args, **kargs):
        (name, key, value) = data
        if self.cm.global_config is None:
            self._init_global_config()

        if 'server_configs' not in self.cm.global_config:
            self.cm.global_config['server_configs'] = dict()
        _configs    = self.cm.global_config['server_configs']

        if name not in _configs:
            _configs[name] = dict()

        _config = _configs[name]
        _config[key] = value

    def _config_user(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'user', value))

    def _config_path(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'path', value))

    def _config_start(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'start', value))

    def _config_stop(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'stop', value))

    def _config_core(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'core', value))

    def _config_logs(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'logs', value))

    def _config_elogs(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'elogs', value))

    def _config_etc(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'etc', value))

    def _config_extra(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'extra', value))

    def _config_root(self, data, *args, **kargs):
        (name, value) = data
        self.robot_opt(config_server=(name, 'root', value))

    def _start_server(self, config, *args, **kargs):
        (name, sleep) = config
        _config = self._server_config(name)
        _start  = _config['start']
        _path   = os.path.split(_start)[0]
        _bin    = os.path.split(_start)[1]
        _cmd    = 'cd %s && ./%s' % (_path, _bin)
        self.logger.info('Starting Server with %s' % _bin)
        self.robot_opt(run_ssh=(name, 'send', _cmd))
        time.sleep(sleep)

    def _delay_start_server(self, config, *args, **kargs):
        (name, sleep) = config
        if self.cm.server is None:
            self.cm.server = list()
        _config = self._server_config(name)
        _start  = _config['start']
        _path   = os.path.split(_start)[0]
        _bin    = os.path.split(_start)[1]
        _cmd    = 'cd %s && ./%s' % (_path, _bin)
        _ssh    = self._ssh_config(name)
        _server = dict()
        _server['ssh'] = _ssh[0]
        _server['cmd'] = _cmd
        _server['sleep'] = sleep
        self.cm.server.insert(0, _server)

    def _stop_server(self, name, *args, **kargs):
        _config = self._server_config(name)
        _stop   = _config['stop']
        _path   = os.path.split(_stop)[0]
        _bin    = os.path.split(_stop)[1]
        self.logger.info('Stoping Server with %s' % _bin)
        self.robot_opt(run_ssh=(name, 'send', 'cd %s && ./%s' % (_path, _bin)))
        time.sleep(0.2)

    def _server_path(self, data, *args, **kargs):
        (name, key) = data
        _config = self._server_config(name)
        return _config[key]

    def _server_user(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'user'))

    def _server_etc(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'etc'))

    def _server_start_script(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'start'))

    def _server_stop_script(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'stop'))

    def _server_core_path(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'core'))

    def _server_logs(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'logs'))

    def _server_elogs(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'elogs'))

    def _server_root(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'root'))

    def _server_extra(self, name, *args, **kargs):
        return self.robot_opt(server_path=(name, 'extra'))

    #===================================================================
    # ssh related
    #===================================================================
    def _config_ssh(self, data, *args, **kargs):
        (key, server, port, user) = data
        self.logger.info('Config SSH %s@%s:%s' % (user, server, port))
        _hosts  = self.cm.global_config.get('hosts', dict())
        _config = dict()
        _config['server']   = server
        _config['port']     = int(port)
        _config['user']     = user
        _ssh    = self.ssh_opt(init_ssh=_config)
        _sftp   = self.ssh_opt(init_sftp=_ssh)
        _hosts[key] = (_ssh, _sftp, _config)
        self.cm.global_config['hosts'] = _hosts

    def _clear_ssh(self, *args, **kargs):
        for _key, _val in self.cm.global_config['hosts'].items():
            _ssh    = _val[0]
            _sftp   = _val[1]
            self.ssh_opt(close_sftp=_sftp)
            self.ssh_opt(close_ssh=_ssh)

    def _ssh_config(self, name, *args, **kargs):
        if name is None:
            name    = self._default_server()
        _hosts  = self.cm.global_config['hosts']
        return _hosts[name]

    def _run_ssh(self, data, *args, **kargs):
        (key, optype, params) = data
        _hosts = self.cm.global_config['hosts']
        _ssh    = _hosts[key][0]
        _sftp   = _hosts[key][1]
        if optype == 'ssh':
            self.logger.info('Running SSH: %s' % params)
            _ret = self.ssh_opt(ssh_cmd=(_ssh, params))
            assert int(_ret['returncode']) == 0, _ret
            self.logger.info(_ret)
            return _ret
        elif optype == 'exec':
            self.logger.info('Running SSH: %s' % params)
            _ret = self.ssh_opt(ssh_cmd=(_ssh, params))
            self.logger.info(_ret)
            return _ret
        elif optype == 'send':
            self.logger.info('Running SSH: %s' % params)
            return self.ssh_opt(ssh_send=(_ssh, params))
        elif optype == 'get':
            (remote, local) = params
            return self.ssh_opt(sftp_get=(_sftp, remote, local))
        elif optype == 'put':
            (local, remote) = params
            return self.ssh_opt(sftp_put=(_sftp, local, remote))
        else:
            self.logger.info('SSH command type not recognized!')

    #===================================================================
    # shell command
    #===================================================================
    def _adjust_min_delay(self, delay, *args, **kargs):
        minval = self.robot_opt(get_cache=('min_delay', None))
        if minval is None:
            return delay
        _min = 100
        for _item in delay:
            if _min > _item and _min > 0:
                _min = _item
        _times = minval / _min
        return [x*_times for x in delay]

    def _adjust_max_delay(self, delay, *args, **kargs):
        maxval = self.robot_opt(get_cache=('max_delay', None))
        if maxval is None:
            return delay
        _max = delay[0]
        for _item in delay:
            if _max < _item:
                _max = _item
        _times = maxval / _max
        return [x*_times for x in delay]

    def _prepare_protoc(self, *args, **kargs):
        _bin    = self.cm.global_config['bin']
        _protoc = os.path.join(_bin, 'protoc')
        return _protoc

    def _prepare_nginx(self, data, *args, **kargs):
        (logs, cache) = data
        _bin    = self.cm.global_config['bin']
        _root   = os.path.join(_bin, 'fullcache')
        _nginx  = os.path.join(_root, 'sbin/nginx')
        _conf   = os.path.join(_root, 'conf/nginx.conf')
        _lpath  = self._path(_root, logs)
        _cpath  = self._path(_root, cache)
        _start  = self.convert(join=(_nginx, ' -p ', _root))
        _stop   = self.convert(join=(_nginx, ' -p ', _root, ' -s stop'))
        _port   = self.robot_opt(random_local_port=('nginx', 1))
        _access = self.convert(join=(logs, '/fullcache.access.log.', _port, '  main'))
        _error  = self.convert(join=(logs, '/fullcache.error.log.', _port, '   info'))
        self._create_path(_lpath)
        self._create_path(_cpath)
        self.cm.global_config['nginx_bin']      = _nginx
        self.cm.global_config['nginx_conf']     = _conf
        self.cm.global_config['nginx_start']    = _start
        self.cm.global_config['nginx_stop']     = _stop
        self.cm.global_config['nginx_port']     = _port
        self.cm.global_config['nginx_logs']     = _lpath
        self.cm.global_config['nginx_access']   = _access
        self.cm.global_config['nginx_error']    = _error
        self.cm.global_config['nginx_cache']    = _cpath
        self.cm.global_config['nginx_cname']    = cache
        self.logger.info('prepare nginx port:%s, logs:%s, cache:%s' % (_port, _lpath, _cpath))

    def _nginx_conf(self, *args, **kargs):
        return self.cm.global_config['nginx_conf']

    def _nginx_bin(self, *args, **kargs):
        return self.cm.global_config['nginx_bin']

    def _nginx_logs(self, *args, **kargs):
        return self.cm.global_config['nginx_logs']

    def _nginx_access(self, *args, **kargs):
        return self.cm.global_config['nginx_access']

    def _nginx_error(self, *args, **kargs):
        return self.cm.global_config['nginx_error']

    def _nginx_port(self, *args, **kargs):
        return self.cm.global_config['nginx_port']

    def _nginx_cname(self, *args, **kargs):
        return self.cm.global_config['nginx_cname']

    def _nginx_cache(self, *args, **kargs):
        return self.cm.global_config['nginx_cache']

    def _start_nginx(self, *args, **kargs):
        _name   = self._default_server()
        _export = self.cm.global_config['export_lib']
        _start  = self.cm.global_config['nginx_start']
        _cmd    = self.convert(join=(_export, _start))
        self.logger.info(_cmd)
        self.robot_opt(run_ssh=(_name, 'exec', _cmd))

    def _stop_nginx(self, *args, **kargs):
        _name   = self._default_server()
        _export = self.cm.global_config['export_lib']
        _stop   = self.cm.global_config['nginx_stop']
        _cmd    = self.convert(join=(_export, _stop))
        self.logger.info(_cmd)
        self.robot_opt(run_ssh=(_name, 'exec', _cmd))
