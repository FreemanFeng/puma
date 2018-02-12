# -*- coding:utf-8 -*-
'''
This Class is used to provide avaiable modules
'''
from singleton import Singleton
from handle_exception import handle_exception

class StaticMobs(Singleton):
    '''
    Binding Static Modules
    '''
    @handle_exception
    def __init__(self, *args, **kargs):
        self.atomic_modules = {
                'binding'           :   'Binding',
                'callback'          :   'Callback',
                'call_function'     :   'CallFunction',
                'inner_call'        :   'InnerCall',
                'convert'           :   'Convert',
                'file_opt'          :   'FileOpt',
                'proc_opt'          :   'ProcOpt',
                'queue_opt'         :   'QueueOpt',
                'sock_opt'          :   'SockOpt',
                'ssh_opt'           :   'SSHOpt',
                'shell_opt'         :   'ShellOpt',
                'paths'             :   'Paths'
                }

        self.opt_modules = {
                'event_opt'         :   'EventOpt',
                'http_opt'          :   'HttpOpt',
                'run_plugin'        :   'RunPlugin',
                'robot_result'      :   'RobotResult',
                'robot_opt'         :   'RobotOpt',
                'local_port'        :   'LocalPort',
                'remote_port'       :   'RemotePort',
                'app_opt'           :   'AppOpt',
                'cms_opt'           :   'CmsOpt',
                'idm_opt'           :   'IdmOpt'
                }

        self.modules = dict()
        self.modules.update(self.atomic_modules)
        self.modules.update(self.opt_modules)

    @property
    def mobs(self, *args, **kargs):
        return self.modules

    @property
    def atom_mobs(self, *args, **kargs):
        return self.atomic_modules

    @property
    def opt_mobs(self, *args, **kargs):
        return self.opt_modules
