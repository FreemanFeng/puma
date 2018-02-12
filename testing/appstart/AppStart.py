# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],
        '../../src/modules'))

sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],
        '../'))

from server_opt import ServerOpt
from MBase import MBase
from binding import Binding

class AppStart(MBase):
    def __init__(self, *args, **kargs):
        super(AppStart, self).__init__()
        _modules = {
                'RobotCommon'       :   'RobotCommon'
                }

        Binding().binding(self, modules = _modules, entity = self)

    #===================================================================
    # utility with return value
    #===================================================================
    def config_list(self, name, key, *args, **kargs):
        _data = dict()
        _data[key] = [x for x in args]
        _params = self.get_param(name, dict())
        _params.update(_data)
        self.update_params(name, _params)

    #===================================================================
    # interfaces
    #===================================================================
    def init_config(self):
        self.robot_opt(load_config='etc/apps/appstart/appstart_robot_config.yml')
        self.robot_opt(init_project='testing/appstart')

    def init_servers(self):
        self.robot_opt(init_servers=self.cm.appstart)

    def apply_devices(self, count, *args):
        _params = self.to_dict(args)
        self.robot_opt(apply_devices=(int(count), _params))

    def install_app(self, install, count, *args):
        if int(install) == 0:
            return
        _params = self.to_dict(args)
        self.robot_opt(install_app=(int(count), _params))

    def init_devices(self):
        self.robot_opt(init_devices=1)

    def return_devices(self):
        self.robot_opt(return_devices=1)

    #===================================================================
    # test entry
    #===================================================================
    def run_debug(self, *args, **kargs):
        self.init_caller(self)
        return self.debug_test(args)

    def run(self, params):
        self.init_caller(self)
        return self.run_test(params)

    #===================================================================
    # pre condition functions
    #===================================================================

    #===================================================================
    # user stories
    #===================================================================
    def start_app(self, *args, **kargs):
        self.run(args)

    #===================================================================
    # test step function
    #===================================================================
    def sync_cms_data_format(self):
        self.init_config()
        _path = self.init_data('cms')
        self.cms_opt(getres=_path)

    def kill_adb_install_shell(self):
        _cmd = "ps ux | grep adb | grep install | grep -v grep | awk '{print $2}' | xargs kill -9"
        self.run_cmd(_cmd)

if __name__ == '__main__':
    _obj = AppStart()
    _obj.init_config()
    _obj.update_params('layout_mode', 1)
    _obj.show_results()
