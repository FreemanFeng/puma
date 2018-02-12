# -*- coding:utf-8 -*-

import socket
import random

import os
import time
from macaca import WebDriver
from macaca import Keys
from retrying import retry

from SBase import SBase
from handle_exception import handle_exception

class MacacaOpt(SBase):
    def __init__(self, *args, **kargs):
        super(MacacaOpt, self).__init__()

    @handle_exception
    def macaca_opt(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    @retry
    def _load(self, data, *args, **kargs):
        (desired_caps, server_url) = data
        self.driver = WebDriver(desired_caps, server_url)
        self.logger.info("Retry connecting server...")
        self.driver.init()

    @handle_exception
    def _quit(self, *args, **kargs):
        self.driver.quit()

    @handle_exception
    def _login_demo(self, *args, **kargs):
        el = self.driver \
            .elements_by_class_name('android.widget.EditText')[0] \
            .send_keys('中文+Test+12345678')   \

        el = self.driver \
            .elements_by_class_name('android.widget.EditText')[1] \
            .send_keys('111111')

        # self.driver.keys(Keys.ENTER.value + Keys.ESCAPE.value)

        self.driver \
            .element_by_name('Login') \
            .click()

    @handle_exception
    def _launch_uc(self, *args, **kargs):
        pass


if __name__ == '__main__':
    _obj = MacacaOpt()
    desired_caps = {
        'platformName': 'android',
        #'app': 'https://npmcdn.com/android-app-bootstrap@latest/android_app_bootstrap/build/outputs/apk/android_app_bootstrap-debug.apk',
        'app': 'http://100.100.200.38:58081/android-free-debug.apk',
        }

    server_url = {
        'hostname': 'localhost',
        'port': 3456
    }
    _obj.macaca_opt(load=(desired_caps, server_url))
    #_obj.macaca_opt(login_demo=1)
    _obj.macaca_opt(launch_uc=1)
    _obj.macaca_opt(quit=1)
