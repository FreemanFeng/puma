# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module wraps the Android Asset Packaging Tool."""
#if UC_BUILD
import os
from devil import  devil_env
#else
#from devil.android.sdk import build_tools
#endif
from devil.utils import cmd_helper
from devil.utils import lazy


#if UC_BUILD
def _FindAapt():
  try:
    status, output = cmd_helper.GetCmdStatusAndOutput(['which', 'aapt'])
    if output:
        return output.replace('\n', '')
  except:
    pass
  path = devil_env.getResourceLocation()
  path = os.path.join(path, 'aapt')
  return path

_aapt_path = lazy.WeakConstant(lambda: _FindAapt())
#else
#_aapt_path = lazy.WeakConstant(lambda: build_tools.GetPath('aapt'))
#endif

def _RunAaptCmd(args):
  """Runs an aapt command.

  Args:
    args: A list of arguments for aapt.

  Returns:
    The output of the command.
  """
  cmd = [_aapt_path.read()] + args
  status, output = cmd_helper.GetCmdStatusAndOutput(cmd)
  if status != 0:
    raise Exception('Failed running aapt command: "%s" with output "%s".' %
                    (' '.join(cmd), output))
  return output


def Dump(what, apk, assets=None):
  """Returns the output of the aapt dump command.

  Args:
    what: What you want to dump.
    apk: Path to apk you want to dump information for.
    assets: List of assets in apk you want to dump information for.
  """
  assets = assets or []
  if isinstance(assets, basestring):
    assets = [assets]
  return _RunAaptCmd(['dump', what, apk] + assets).splitlines()
