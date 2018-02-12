# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],
        '../src/modules'))
from server_opt import ServerOpt
from MBase import MBase

class RobotCommon(MBase):
    caller = None
    def __init__(self, *args, **kargs):
        super(RobotCommon, self).__init__()

    #===================================================================
    # utility with return value
    #===================================================================
    def url_encode(self, url):
        return self.robot_opt(url_encode=url)

    def dict_value(self, data, key):
        return self.robot_opt(dict_value=(data, key))

    def store_dict(self, data, key, value):
        return self.robot_opt(store_dict=(data, key, value))

    def cache_result(self, key, value, ret_type = None):
        return self.robot_opt(cache_result=(key, value, ret_type))

    def init_cache(self):
        return self.robot_opt(init_cache=1)

    def get_cache(self, key, ret_type = None):
        return self.robot_opt(get_cache =(key, ret_type))

    def get_cache_default(self, key, default, ret_type = None):
        _ret = self.get_cache(key, ret_type)
        if _ret is None:
            return default
        return _ret

    def init_output(self, format = 'jpeg'):
        return self.robot_opt(init_output=format)

    def init_data(self, folder = 'output'):
        return self.robot_opt(init_data=folder)

    def init_path(self, path = 'etc'):
        return self.robot_opt(init_path=path)

    def update_path_params(self, path):
        return self.robot_opt(update_path_params=path)

    def locate_image(self, name, pos = 'upload'):
        return self.robot_opt(locate_image=(name, pos))

    def init_upload_image(self, name, pos = 'upload'):
        _path   = self.locate_image(name, pos)
        return self.update_path_params(_path)

    def init_baseline_image(self, name):
        return self.init_upload_image(name, 'baseline')

    def spaces(self, cnt):
        return ' ' * int(cnt)

    def single_quote(self, data = ''):
        return self.convert(join=("\\'", data, "\\'"))

    def double_quote(self, data = ''):
        return self.convert(join=('\\"', data, '\\"'))

    #===================================================================
    # shell related utility
    #===================================================================
    def backup_testcase_logs(self, path, port, testcase):
        _name   = self.default_server()
        _cmd    = 'find %s | grep %s' % (path, port)
        _ret    = self.run_ssh(_cmd, _name, 'exec')
        if _ret['returncode'] != 0:
            return
        _tc_name = testcase.lower().replace(' ', '')
        for _file in _ret['stdout']:
            _file   = _file.strip()
            _path   = os.path.split(_file)[0]
            _base   = os.path.basename(_file).split('.')[0]
            _prefix = os.path.join(_path, _base)
            _cmd = 'cp %s %s.%s.log' % (_file, _prefix, _tc_name)
            self.run_ssh(_cmd, _name, 'send')

    def clear_port_logs(self, path, port):
        _name   = self.default_server()
        _cmd    = 'find %s | grep %s' % (path, port)
        _ret    = self.run_ssh(_cmd, _name, 'exec')
        if _ret['returncode'] != 0:
            return
        for _file in _ret['stdout']:
            _cmd = '> %s' % _file
            self.run_ssh(_cmd, _name, 'send')

    def backup_cores(self, path):
        _name   = self.default_server()
        _cmd    = 'ls %s/core.*' % (path)
        _ret    = self.run_ssh(_cmd, _name, 'exec')
        if _ret['returncode'] != 0:
            return
        for _file in _ret['stdout']:
            _path   = os.path.split(_file.strip())[0]
            _file   = os.path.basename(_file.strip())
            _cmd    = 'cd %s && mv %s bak.%s' % (_path, _file, _file)
            self.run_ssh(_cmd, _name, 'send')

    def get_args(self, *args):
        self.logger.info("Args: %s, Type: %s" % (args, type(args)))
        if args and type(args[0]) in (list, tuple):
            return args[0]
        return args

    def get_header_args(self, cnt, *args):
        return args[:int(cnt)]

    def get_rest_args(self, cnt, *args):
        return args[int(cnt):]

    def wrap_shell(self, tool, data, extra = ''):
        #_data = data.replace('/', '\/').replace('"', '\"')
        _data = data.replace('"', '\"')
        return self.convert(join=(tool, ' "', _data, '" ', extra))

    def wrap_echo(self, data, extra = ''):
        return self.wrap_shell('echo ', data, extra)

    def local_ip(self):
        return self.robot_opt(local_ip=1)

    def md5sum(self, path):
        return self.robot_opt(md5sum=path)

    #===================================================================
    # html related utility
    #===================================================================
    def html_subres(self, maindoc, url):
        return self.robot_opt(html_subres=(maindoc, url))

    def outlink_subres(self, maindoc, url):
        return self.robot_opt(outlink_subres=(maindoc, url))

    def origin_subres(self, maindoc, url):
        return self.robot_opt(origin_subres=(maindoc, url))

    def converted_subres(self, maindoc, url):
        return self.robot_opt(converted_subres=(maindoc, url))

    def download_maindoc(self, url):
        if not url.startswith('http'):
            return
        _bin = os.path.join(self.cm.global_config['bin'], 'curl')

    def prepare_curl(self, url, *args, **kargs):
        _tool   = 'curl'
        _args   = self.cm.curl['args']
        _ua     = self.cm.curl['ua']
        _index  = self.convert(randint=len(_ua) - 1)
        _args   = self.convert(join=(_args, ' \"', _ua[_index], '\" \"', url, '\"'))
        _args   = self.convert(join=("'", _args, "'"))
        _hpath  = self.init_output('html')
        _path   = self.get_param('data_output')
        _opcode = self.convert(join=("'", '-o', "'"))
        _hfile  = os.path.basename(_hpath)
        _trace  = self.convert(sign=8)
        _tfile  = self.convert(join=('curl_trace_', _trace, '.trace'))
        _tpath  = os.path.join(_path, _tfile)
        self.update_params('curl_html', _hfile)
        self.cache_result('curl_trace', _tpath)
        return self.robot_opt(prepare_readfifo=(_tool, _args, _path, _opcode, _hfile, _tfile))

    def max_delay(self, maxval):
        self.cache_result('max_delay', float(maxval))

    def min_delay(self, minval):
        self.cache_result('min_delay', float(minval))

    def parse_ctrace(self):
        _trace = self.get_cache('curl_trace')
        return self.robot_opt(parse_ctrace=_trace)
    #===================================================================
    # Server Config related interfaces
    #===================================================================
    def server_port(self, name):
        return self.robot_opt(server_port=name)

    def server_user(self, name):
        return self.robot_opt(server_user=name)

    def server_etc(self, name):
        return self.robot_opt(server_etc=name)

    def server_start_script(self, name):
        return self.robot_opt(server_start_script=name)

    def server_stop_script(self, name):
        return self.robot_opt(server_stop_script=name)

    def server_core_path(self, name):
        return self.robot_opt(server_core_path=name)

    def server_logs(self, name):
        return self.robot_opt(server_logs=name)

    def server_elogs(self, name):
        return self.robot_opt(server_elogs=name)

    def server_root(self, name):
        return self.robot_opt(server_root=name)

    def server_extra(self, name):
        return self.robot_opt(server_extra=name)

    def wait_alive(self):
        return self.robot_opt(wait_alive=1)

    def keep_alive(self):
        return self.robot_opt(keep_alive=1)

    def start_server(self, name, sleep = 1.0):
        return self.robot_opt(start_server=(name, sleep))

    def stop_server(self, name):
        return self.robot_opt(stop_server=name)

    def config_root(self, server_name, root):
        self.robot_opt(config_root=(server_name, root))

    def config_user(self, server_name, user_name):
        self.robot_opt(config_user=(server_name, user_name))

    def config_path(self, server_name, path):
        self.robot_opt(config_path=(server_name, path))

    def config_start(self, server_name, start_script):
        self.robot_opt(config_start=(server_name, start_script))

    def config_stop(self, server_name, stop_script):
        self.robot_opt(config_stop=(server_name, stop_script))

    def config_core(self, server_name, core_path):
        self.robot_opt(config_core=(server_name, core_path))

    def config_logs(self, server_name, logs_path):
        self.robot_opt(config_logs=(server_name, logs_path))

    def config_elogs(self, server_name, logs_path):
        self.robot_opt(config_elogs=(server_name, logs_path))

    def config_etc(self, server_name, etc_path):
        self.robot_opt(config_etc=(server_name, etc_path))

    def config_extra(self, server_name, conf_path):
        self.robot_opt(config_extra=(server_name, conf_path))

    #===================================================================
    # NGINX related interfaces
    #===================================================================
    def prepare_nginx(self, logs, cache):
        return self.robot_opt(prepare_nginx=(logs, cache))

    def nginx_conf(self):
        return self.robot_opt(nginx_conf=1)

    def nginx_logs(self):
        return self.robot_opt(nginx_logs=1)

    def nginx_access(self):
        return self.robot_opt(nginx_access=1)

    def nginx_error(self):
        return self.robot_opt(nginx_error=1)

    def nginx_cache(self):
        return self.robot_opt(nginx_cache=1)

    def nginx_cname(self):
        return self.robot_opt(nginx_cname=1)

    def nginx_bin(self):
        return self.robot_opt(nginx_bin=1)

    def nginx_port(self):
        return self.robot_opt(nginx_port=1)

    def start_nginx(self):
        self.robot_opt(start_nginx=1)

    def stop_nginx(self):
        self.robot_opt(stop_nginx=1)

    #===================================================================
    # Server related interfaces
    #===================================================================
    def delay_start_server(self, name, sleep = 1.0):
        return self.robot_opt(delay_start_server=(name, sleep))

    def tcpdump(self, service_type):
        _port = self.tcp_port(service_type)
        return self.robot_opt(tcpdump=(service_type, _port))

    def socat_server(self, name, cmd):
        return self.robot_opt(socat_server=(name, cmd))

    def extra_server(self, name, proto, port = None, timeout = 1):
        return self.robot_opt(extra_server=(name, proto, port, timeout))

    #===================================================================
    # General interfaces
    #===================================================================
    def init_caller(self, caller):
        self.caller = caller

    def init_global_config(self):
        self.robot_opt(init_global_config=1)

    def config_param(self, key, value):
        self.robot_opt(config_param=(key, value))

    def config_params(self, config):
        self.robot_opt(config_params=config)

    def pre_config(self, keyword, *args):
        self.robot_opt(pre_config=(self, keyword, args))

    def to(self, keyword, *args):
        self.robot_opt(to=(self, keyword, args))

    def run_steps(self):
        self.robot_opt(run_steps=self)

    def pre_condition(self):
        self.robot_opt(pre_condition=self)

    def check_point(self, cp_type, key, opcode, value=None):
        self.robot_opt(check_point=(cp_type, key, opcode, value, None))

    def check_extra_point(self, cp_type, extra_key, key, opcode, value=None):
        self.robot_opt(check_point=(cp_type, key, opcode, value, extra_key))

    def init_params(self):
        self.robot_opt(init_params=1)

    def show_results(self):
        self.robot_opt(show_results=1)

    def get_result(self, ret_type, key = None):
        return self.robot_opt(get_result=(ret_type, key))

    def check_results(self):
        self.robot_opt(check_if_ok=1)

    def check_if_ok(self, queue):
        if queue is not None and not queue.empty():
            self.cm.results.update(queue.get())

        if self.cm.results:
            self.check_results()

    def config_test(self, *args):
        self.robot_opt(config_test=args)

    def to_utf8(self, params):
        return self.robot_opt(to_utf8=params)

    def to_list(self, *args):
        return args

    def to_dict(self, params):
        return self.robot_opt(to_dict=params)

    def update_params(self, *args):
        self.robot_opt(update_params=args)

    def clear_params(self):
        self.robot_opt(clear_params=1)

    def get_param(self, key, default = None):
        return self.robot_opt(get_param=(key, default))

    def update_dict_param(self, name, params):
        self.robot_opt(update_dict_param=(name, params))

    def update_headers(self, params):
        headers = self.to_dict(params)
        self.robot_opt(update_dict_param=('headers', headers))
        return headers

    def build_list(self, key, *args, **kargs):
        if not args:
            return
        _params = self.get_param(key, list())
        _params.append(tuple(args))
        self.update_params(key, _params)

    def build_map(self, key, *args, **kargs):
        if not args:
            return
        _data = self.to_dict(args)
        _params = self.get_param(key, dict())
        _params.update(_data)
        self.update_params(key, _params)

    def build_maps(self, key, node, *args):
        if not args:
            return
        _data = self.to_dict(args)
        _params = self.get_param(key, dict())
        _params.update({node: _data})
        self.update_params(key, _params)

    #===================================================================
    # SSH related interfaces
    #===================================================================
    def ssh_default(self, name):
        self.robot_opt(ssh_default=name)

    def set_server(self, name, host, port = None):
        self.robot_opt(set_server=(name, host, port))

    def default_server(self):
        return self.robot_opt(default_server=1)

    def config_ssh(self, server, port, user, key = 'ssh'):
        return self.robot_opt(config_ssh=(key, server, port, user))

    def clear_ssh(self):
        return self.robot_opt(clear_ssh=1)

    def run_ssh(self, params, key = 'ssh', optype = 'ssh'):
        return self.robot_opt(run_ssh=(key, optype, params))

    def output_path(self):
        return self.robot_opt(output_path=1)

    def pids_path(self):
        return self.robot_opt(pids_path=1)

    def sftp_get(self, remote, key = 'ssh'):
        _out = self.robot_opt(output_path=1)
        return self.run_ssh((remote, _out), key, 'get')

    def sftp_put(self, local_file, remote, key = 'ssh'):
        _upload = self.robot_opt(upload_path=1)
        _file   = os.path.join(_upload, local_file)
        return self.run_ssh((_file, remote), key, 'put')

    def upload_socat(self):
        return self.robot_opt(upload_socat=1)

    def ports_range(self, name, min_port, max_port):
        return self.robot_opt(ports_range=(name, int(min_port), int(max_port)))

    def ssh_config(self, name = None):
        return self.robot_opt(ssh_config=name)

    #===================================================================
    # testing related functions
    #===================================================================
    def backup_preconf(self):
        _preconf = list()
        if self.cm.preconf_once:
            _preconf.extend(self.cm.preconf_once)
        self.cache_result('preconf', _preconf)

    def restore_preconf(self):
        _preconf = self.get_cache_default('preconf', list())
        if self.cm.preconf_once is None:
            self.cm.preconf_once = list()
        self.cm.preconf_once.extend(_preconf)

    def backup_steps(self):
        _steps = list()
        if self.cm.steps_once:
            _steps.extend(self.cm.steps_once)
        self.cache_result('steps', _steps)

    def restore_steps(self):
        _steps = self.get_cache_default('steps', list())
        if self.cm.steps_once is None:
            self.cm.steps_once = list()
        self.cm.steps_once.extend(_steps)

    def clear_procs(self):
        _server = self.cm.global_config.get('test_entry', None)
        if _server is not None:
            _server.clear_procs()

    #===================================================================
    # test entry
    #===================================================================
    def run_server(self, params):
        self.caller.init_config()
        self.init_params()
        self.caller.init_servers()
        if self.cm.preconf_once:
            self.pre_condition()
        _config = self.to_dict(params)
        if self.cm.params_once:
            _config.update(self.cm.params_once)
        self.config_params(_config)
        _server = ServerOpt()
        self.cm.global_config['test_entry'] = _server
        _server.start_server(dict())
        if self.cm.steps_once:
            self.run_steps()

    def run_test(self, params):
        self.caller.init_config()
        self.init_params()
        self.caller.init_servers()
        if self.cm.preconf_once:
            self.pre_condition()
        _config = self.to_dict(params)
        if self.cm.params_once:
            _config.update(self.cm.params_once)
        self.config_params(_config)
        _server = ServerOpt()
        self.cm.global_config['test_entry'] = _server
        try:
            _server.start_multi_server(dict())
            if self.cm.steps_once:
                self.run_steps()
            self.check_if_ok(_server.get_queue())
        except:
            _server.clear_procs()
            raise
        _server.clear_procs()

    def debug_test(self, params):
        self.caller.init_config()
        self.init_params()
        self.caller.init_servers()
        if self.cm.preconf_once:
            self.pre_condition()
        _config = self.to_dict(params)
        if self.cm.params_once:
            _config.update(self.cm.params_once)
        self.config_params(_config)
        if self.cm.steps_once:
            self.run_steps()

    #===================================================================
    # pre condition functions
    #===================================================================
    def extra_config(self, config_file):
        self.robot_opt(load_config=config_file)

    def local_server(self):
        self.update_params('local server', self.local_ip())

    def fixed_port(self, service_type, port):
        _type   = service_type.replace(' ', '_').lower()
        _name   = self.convert(join=(_type, '_fixed_port'))
        self.logger.info('Server %s listening on %s' % (service_type, port))
        self.cache_result(_name, int(port))

    def service_port(self, service_type, proto, port, timeout):
        _type   = service_type.replace(' ', '_').lower()
        _name   = self.convert(join=(_type, '_fixed_port'))
        _fixed  = self.get_cache_default(_name, None)
        if _fixed is not None:
            self.logger.info('Service %s Port %s' % (service_type, _fixed))
            return self.extra_server(service_type, proto, _fixed, timeout)
        return self.extra_server(service_type, proto, port, timeout)

    def set_timeout(self, timeout):
        self.robot_opt(set_timeout=float(timeout))

    def no_tcp_init(self):
        self.update_params('no_tcp_init', 1)

    def prepare_protoc(self):
        self.cm.protoc = self.robot_opt(prepare_protoc=1)

    def tcp_port(self, service_type):
        _type   = service_type.replace(' ', '_').lower()
        _pkey   = self.convert(join=(_type, '_port'))
        _port   = self.cm.global_config.get(_pkey, None)
        if _port is None:
            _port = self.robot_opt(random_local_port=(service_type, 1))
            self.cm.global_config[_pkey] = _port
        self.logger.info('%s tcp port : %s' % (service_type, _port))
        return _port

    def usock(self, service_type):
        _type   = service_type.replace(' ', '_').lower()
        _pkey   = self.convert(join=(_type, '_usock'))
        _usock  = self.cm.global_config.get(_pkey, None)
        if _usock is None:
            _name   = self.default_server()
            _path   = self.server_logs(_name)
            _rand   = self.convert(sign=8)
            _file   = self.convert(join=(_type, '_', _rand, '.usock'))
            _usock  = os.path.join(_path, _file)
            self.cm.global_config[_pkey] = _usock
        self.logger.info('%s usock: %s' % (service_type, _usock))
        return _usock

    def unix_to_tcp(self, service_type, usock, tsock):
        _type   = service_type.replace(' ', '_').lower()
        _pkey   = self.convert(join=(_type, '_cmd'))
        _cmd    = self.cm.global_config.get(_pkey, None)
        if _cmd is None:
            _socat = self.cm.global_config['socat_bin']
            _cmd   = self.convert(join=(_socat, ' unix-listen:', usock, ',fork tcp-connect:', tsock))
            self.cm.global_config[_pkey] = _cmd
        self.logger.info('%s unix to tcp cmd: %s' % (service_type, _cmd))
        return _cmd

    def config_tcp(self, service_type, message, *args):
        _type   = service_type.replace(' ', '_').lower()
        _name   = self.convert(join=(_type, '_config'))
        _config = self.get_cache_default(_name, dict())
        _msg    = self.get_cache_default(message, dict())
        _config[message] = _msg
        _config['rules'] = [x for x in args]
        self.update_params(_name, _config)

    def config_message(self, parent, field_name, field_type):
        _parent = self.get_cache_default(parent, dict())
        _data   = self.get_cache_default(field_type, dict())
        _parent[field_name] = _data
        self.cache_result(parent, _parent)

    def config_field(self, parent, field, value):
        _parent = self.get_cache_default(parent, dict())
        _parent[field] = value
        self.cache_result(parent, _parent)

    def http_path(self, path):
        self.update_params('http_path', path)

    def set_headers(self, param_type, *args):
        _headers = self.update_headers(args)
        self.robot_opt(update_dict_param=(param_type, _headers))

    #===================================================================
    # server related pre condition functions
    #===================================================================
    def http_server(self, service_type, proto, port = None, timeout = 1):
        if not self.could_server_start(service_type):
            return
        _port   = self.service_port(service_type, proto, port, timeout)
        _server = self.get_param('local server')
        self.update_params('http_server', _server)
        self.update_params('http_port', _port)
        self.update_params('project', self.cm.global_config['project'])
        self.update_params('htdocs', self.cm.global_config['htdocs'])

    def extra_http_server(self, service_type, proto, port = None, timeout = 1):
        if not self.could_server_start(service_type):
            return
        _port   = self.service_port(service_type, proto, port, timeout)
        _server = self.get_param('local server')
        _type   = service_type.replace(' ', '_').lower()
        _skey   = self.convert(join=(_type, '_server'))
        _pkey   = self.convert(join=(_type, '_port'))
        self.cm.global_config[_pkey] = _port
        self.update_params(_skey, _server)
        self.update_params(_pkey, _port)
        self.update_params('htdocs', self.cm.global_config['htdocs'])
        self.update_params('load_config', self.cm.global_config['load_config'])

    def tcp_server(self, service_type, proto, port = None, timeout = 1):
        if not self.could_server_start(service_type):
            return
        _port   = self.service_port(service_type, proto, port, timeout)
        self.logger.info('Starting TCP Server on port %s' % _port)
        _server = self.get_param('local server')
        _type   = service_type.replace(' ', '_').lower()
        _skey   = self.convert(join=(_type, '_server'))
        _pkey   = self.convert(join=(_type, '_port'))
        self.cm.global_config[_pkey] = _port
        self.prepare_protoc()
        self.update_params(_skey, _server)
        self.update_params(_pkey, _port)
        self.update_params('init_url', 'helloworld.html')
        self.update_params('load_config', self.cm.global_config['load_config'])

    def no_server_start(self, service_type):
        _type   = service_type.replace(' ', '_').lower()
        _config = self.get_cache_default('no_server_start', dict())
        _config[_type] = 1
        self.cache_result('no_server_start', _config)

    def could_server_start(self, service_type):
        _type   = service_type.replace(' ', '_').lower()
        _config = self.get_cache_default('no_server_start', None)
        if _config is None or _type not in _config:
            return True
        return False

    #===================================================================
    # TCP Service Config Related Functions
    #===================================================================
    def config_tcp(self, service_type, message, *args):
        _type   = service_type.replace(' ', '_').lower()
        _name   = self.convert(join=(_type, '_config'))
        _config = self.get_cache_default(_name, dict())
        _msg    = self.get_cache_default(message, dict())
        _config[message] = _msg
        _config['rules'] = [x for x in args]
        self.update_params(_name, _config)

    def config_service(self, service_type, key = None, *args):
        _type   = service_type.replace(' ', '_').lower()
        _name   = self.convert(join=(_type, '_config'))
        _config = self.get_param(_name, dict())
        if key is not None:
            _config[key] = [x for x in args]
        self.update_params(_name, _config)

    #===================================================================
    # test step function
    #===================================================================
    def run_cmd(self, cmd):
        return self.shell_opt(cmd=cmd)

    #===================================================================
    # checkpoints function
    #===================================================================
    def check_no_cores(self, path):
        _name       = self.default_server()
        _cmd        = 'ls %s/core.*' % (path)
        _ret        = self.run_ssh(_cmd, _name, 'exec')
        _out        = _ret['stdout']
        _ret        = len(_out)
        _expected   = 0
        return self.robot_opt(wrap_check=('coredumps', _ret, '=', _expected))

    def check_one_usock_key(self, service_type, cache_type, keys, opcode, expected):
        _result = self.convert(space=[x for x in keys])
        self.logger.info("_result %s" % str(_result))
        return self.robot_opt(wrap_check=('%s %s' % (service_type, cache_type),
                                          _result, opcode, expected))

    def check_usock_keys(self, ret_type, service_type, cache_type, opcode, *args):
        _type   = service_type.replace(' ', '_').lower()
        _ret    = self.get_result(ret_type, _type)
        #如果没有写入内容，该key值是找不到的
        if (opcode == 'without') and (cache_type not in _ret):
            return True
        assert cache_type in _ret , "[FATAL ERROR] expected key[%s] to be precent in [%s:%s],bu was not" %(cache_type, service_type, _ret)
        # 根据参数判断， Setkey Time /Setkey Flag /Setkey Cnt/Setkey Head
        if args[0] == 'time' or args[0] == 'flag' or args[0] == 'cnt' or args[0] == 'head':
            _type   = args[0]
            _key    = args[1]
            _value  = args[2]
            _urls   = _ret[cache_type]
            for _url in _urls.keys():
                if _key in _url:
                    _keys = _urls[_url][_type]
            # 转换为字典
            _keys="{'" +  str(_keys) + "':''}"
            _keys=eval(_keys)
            self.check_one_usock_key(service_type, cache_type, _keys, opcode, _value)
        # GetKey/SetKey
        else:
            _keys = _ret[cache_type]
            [self.check_one_usock_key(service_type, cache_type, _keys, opcode, str(x)) for x in args]
