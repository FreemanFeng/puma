# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Provides a work around for various adb commands on android gce instances.

Some adb commands don't work well when the device is a cloud vm, namely
'push' and 'pull'. With gce instances, moving files through adb can be
painfully slow and hit timeouts, so the methods here just use scp instead.
"""
# pylint: disable=unused-argument

import logging
import os
import subprocess

from devil.android import device_errors
from devil.android.sdk import adb_wrapper

logger = logging.getLogger(__name__)


class HiveAdbWrapper(adb_wrapper.AdbWrapper):

  def __init__(self, device_serial):
    super(HiveAdbWrapper, self).__init__(device_serial)
    self._Connect()
    self._Connect()
    self._Connect()
    self._Connect()

  def _Connect(self, timeout=adb_wrapper.DEFAULT_TIMEOUT,
               retries=adb_wrapper.DEFAULT_RETRIES):
    """Connects ADB to the android gce instance."""
    cmd = ['connect', self._device_serial]
    output = self._RunAdbCmd(cmd, timeout=timeout, retries=retries)
    logger.info('remote connect to device: %s' % output)
    if 'unable to connect' in output:
      raise device_errors.AdbCommandFailedError(cmd, output)
    #self.WaitForDevice()


  # override
  def Root(self, **kwargs):
    super(HiveAdbWrapper, self).Root()
    self._Connect()

  # override
  def Install(self, apk_path, forward_lock=False, reinstall=False,
              sd_card=False, **kwargs):
    """Installs an apk on the gce instance

    Args:
      apk_path: Host path to the APK file.
      forward_lock: (optional) If set forward-locks the app.
      reinstall: (optional) If set reinstalls the app, keeping its data.
      sd_card: (optional) If set installs on the SD card.
    """
    adb_wrapper.VerifyLocalFileExists(apk_path)
    cmd = ['install']
    if forward_lock:
      cmd.append('-l')
    if reinstall:
      cmd.append('-r')
    if sd_card:
      cmd.append('-s')
    self.Push(apk_path, '/data/local/tmp/tmp.apk')
    cmd = ['pm'] + cmd
    cmd.append('/data/local/tmp/tmp.apk')
    output = self.Shell(' '.join(cmd))
    self.Shell('rm /data/local/tmp/tmp.apk')
    if 'Success' not in output:
      raise device_errors.AdbCommandFailedError(
          cmd, output, device_serial=self._device_serial)
