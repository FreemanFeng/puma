#!/bin/bash
SRTPATH=$(cd "$(dirname "$0")"; pwd)

#+------------------------------+
#| Install pip with dependency  |
#+------------------------------+
# wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py --user
pip install robotframework --user
pip install paramiko --user
pip install twisted --user
pip install pyOpenSSL  --user
pip install httplib2 --user
pip install requests --user
pip install service_identity --user
pip install wd --user
pip install retrying --user
pip install PyYAML --user
