# -*- coding:utf-8 -*-
from devil.android.device_utils import DeviceUtils
from devil.android.sdk.intent import Intent
from devil.android import device_errors
from lxml import etree
import threading
import time
import tempfile
import os
import traceback
import re

from binding import Binding
from SBase import SBase
from handle_exception import handle_exception

class PopwinOpt(SBase):
    BLOCK_XPATH_LIST=[".//node[@resource-id='com.android.vending:id/alertTitle']",
                      ".//node[@resource-id='com.android.vending:id/banner']",
                      ".//node[@resource-id='com.android.vending:id/message']",
                      u".//node[@text='解析错误' and @package='com.android.packageinstaller']",
                      u".//node[contains(@text, '安装包有异常') and @resource-id='android:id/message']"]

    CANCEL_XPATH_LIST=[u".//node[@text='取消' and @resource-id='android:id/button2']"]

    INSTALL_XPATH_LIST=[".//node[@resource-id='com.android.packageinstaller:id/ok_button']",  # huawei TL00
                        u".//node[@text='允许' and @package='com.huawei.systemmanager']",
                        u".//node[@text='允许' and @package='android']",
                        u".//node[@text='允许' and @package='com.lbe.security.miui']",
                        u".//node[@text='继续安装' and @package='com.miui.securitycenter' ]",
                        ".//node[@resource-id='com.lenovo.safecenter:id/btn_install']",
                        u".//node[@text='确定' and @package='com.lenovo.safecenter']",
                        u".//node[@text='确定' and @package='android']",
                        u".//node[@text='好' and @package='android']",
                        u".//node[@text='允许' and @class='android.widget.Button']",
                        u".//node[@text='安装' and @package='com.android.packageinstaller']",
                        u".//node[@text='完成' and @package='com.android.packageinstaller']",
                        u".//node[@text='继续安装' and @package='com.android.packageinstaller']",
                        u".//node[@text='替换' and @package='com.android.packageinstaller']",
                        u".//node[@text='继续安装旧版本' and @package='com.android.packageinstaller']",
                        ".//node[@resource-id='com.android.packageinstaller:id/virus_warning']",
                        u".//node[@text='安装' and @class='android.widget.Button']",
                        ".//node[@resource-id='vivo:id/vivo_adb_install_ok_button']",
                        ".//node[@resource-id='android:id/button1' and @package='android']",
                        ".//node[@resource-id='android:id/le_bottomsheet_btn_confirm_5']",
                        ".//node[@resource-id='android:id/button1' and @package='com.android.systemui']",
                        ".//node[@resource-id='android:id/button1' and @package='com.smartisanos.systemui']",
                        ".//node[@resource-id='android:id/button1' and @package='com.android.vending']",
                        ".//node[@resource-id='com.android.vending:id/positive_button']",
                        u".//node[@text='允许' and @package='com.aliyun.mobile.permission']",
                        u".//node[@text='继续' and @package='com.android.packageinstaller']",
                        u".//node[@text='确定' and @package='com.android.packageinstaller']",
                        u".//node[@text='完成' and @resource-id='com.lenovo.security:id/back_button']",
                        ".//node[@resource-id='com.android.packageinstaller:id/decide_to_continue']",
                        ".//node[@resource-id='com.android.packageinstaller:id/goinstall']",
                        u".//node[@text='跳过' and @class='android.widget.TextView']" # skip welcome page for uc
                        ]

    INPUT_XPATH_LIST=[".//node[@resource-id='com.coloros.safecenter:id/verify_input']",
                      ".//node[@resource-id='com.coloros.safecenter:id/et_login_passwd_edit']"]


    def __init__(self, device_serial, logger=None):
        super(PopwinOpt, self).__init__()
        if isinstance(device_serial, basestring):
            self.device_util = DeviceUtils(device_serial)
        elif isinstance(device_serial, DeviceUtils):
            self.device_util = device_serial
        else:
            raise ValueError('Unsupported device value: %r' % device_serial)
        self.logger = logger
        self.is_cancel = False
        self.has_input = False
        self.block_msg = ''
        self.t = None
        self.total_time = 0
        self.pointPattern = re.compile("\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]")


    def monitorWindow(self):
        host_dump_name = None
        self.wakeUp()
        self.unlockScreen()
        while not self.is_cancel and self.total_time  < 1800:
            try:
                device_dump_name = '/data/local/tmp/window_dump.xml'
                self.device_util.RunShellCommand(['/system/bin/uiautomator', 'dump', device_dump_name])
                tmp_path = tempfile.mkdtemp()
                host_dump_name = os.path.join(tmp_path, 'window_dump.xml')
                self.device_util.PullFile(device_dump_name, host_dump_name)
                if os.path.exists(host_dump_name) and os.path.getsize(host_dump_name) > 0:
                    root = etree.parse(host_dump_name)
                    if not self.block_msg:
                        for block_xpath in self.BLOCK_XPATH_LIST:
                            for elem in root.xpath(block_xpath):
                                self.block_msg += "\n"
                                self.block_msg += elem.text

                                if self.block_msg.find('异常') != -1:
                                    self.clickByXpathList(self.BLOCK_XPATH_LIST, root)
                    input_xpath = None
                    for xpath_str in self.INPUT_XPATH_LIST:
                        for elem in root.xpath(xpath_str):
                            input_xpath = xpath_str


                    if input_xpath and not self.has_input:
                        self.device_util.RunShellCommand(['input', 'text', 'qwerty'])
                        self.has_input = True
                    self.clickByXpathList(self.INSTALL_XPATH_LIST, root)
                    time.sleep(1)
            except device_errors.DeviceUnreachableError:
                self.is_cancel = True
            except Exception:
                traceback.print_exc()
            finally:
                self.total_time += 1
                if os.path.exists(host_dump_name):
                    os.remove(host_dump_name)

    def clickByXpathList(self, xpath_list, root):
        pos_x = None
        pos_y = None
        for xpath_str in xpath_list:
            for elem in root.xpath(xpath_str):
                bounds = elem.get('bounds')
                if bounds:
                    match = self.pointPattern.match(bounds)
                    if match:
                        l = int(match.groups()[0])
                        t = int(match.groups()[1])
                        r = int(match.groups()[2])
                        b = int(match.groups()[3])
                        pos_x = l + (r - l) * 3 / 4
                        pos_y = (t + b) / 2
        if pos_x and pos_y:
            self.device_util.RunShellCommand(['input', 'tap', str(pos_x), str(pos_y)])

    def startMonitor(self):
        self.t = threading.Thread(target=self.monitorWindow)
        self.t.setDaemon(True)
        self.t.start()


    def stopMonitor(self):
        self.is_cancel = True
        try:
            #//这里按一下back键，因为有些手机装好应用之后还有一个安装成功的弹窗，可能会影响下一次安装
            self.device_util.RunShellCommand(['input', 'keyevent', '4'])
        except device_errors.DeviceUnreachableError:
            self.is_cancel = True
        except Exception:
            traceback.print_exc()

    def unlockScreen(self):
        try:
            self.device_util.RunShellCommand(
                ['input swipe 400 800 400 100; input swipe 50 750 400 750; input swipe 340 1180 340 280'])
            intent = Intent(action='com.ucweb.cloudtest.ACTION_UNLOCK',
                            activity='.Activity.UnlockActivity',
                            package='com.ucweb.cloudtest')
            self.device_util.StartActivity(intent, blocking=False)
        except device_errors.DeviceUnreachableError:
            self.is_cancel = True
        except Exception:
            traceback.print_exc()

    def wakeUp(self):
        try:
            if not self.device_util.IsScreenOn():
                #press menu
                self.device_util.RunShellCommand(['input', 'keyevent', '82'])
        except device_errors.DeviceUnreachableError:
            self.is_cancel = True
        except Exception:
            traceback.print_exc()


# if __name__ == '__main__':
#     helper = MonitorPopWindow(device_serial='0085c63585b6bc90')
