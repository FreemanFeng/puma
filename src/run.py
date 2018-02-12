# -*- coding: utf-8 -*-
import sys
import os
import modules
from modules.server_opt import ServerOpt

def main():
    _server = ServerOpt()
    _server.start_server(sys.argv[1])

if __name__ == '__main__':
    main()
