# -*- coding:utf-8 -*-
'''
This Class is to get path
'''
import os
from os.path import isfile, isdir
import sys
import glob

from singleton import Singleton
from handle_exception import handle_exception

class Paths(Singleton):
    '''
    Paths Related Operation
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''

        super(Paths, self).__init__()

        self.root_path = os.path.join(os.path.split(
                            os.path.realpath(__file__))[0], '../..')
        self.add_paths(*args, **kargs)

    @handle_exception
    def add_paths(self, *args, **kargs):
        if 'paths' in kargs:
            _paths = self._to_list(kargs['paths'])
            for _path in _paths:
                self.add_path(_path)

    @handle_exception
    def _add_sys_path(self, path):
        if isdir(path) and path not in sys.path:
            sys.path.append(path)

    @handle_exception
    def add_path(self, path):
        '''
        add sys path
        '''
        if not isdir(path):
            return 0

        self._add_sys_path(path)

        for x in glob.glob(path + '/*'):
            self._add_sys_path(x)
            self.add_path(x)

    @handle_exception
    def get_root_path(self):
        '''
        get the root path
        '''
        return self.root_path

    def _upper_path(self, path):
        '''
        return upper path
        '''
        return os.path.split(path)[0]

    def _get_file(self, paths):
        '''
        select a valid file path from available path list
        '''
        for _path in paths:
            try:
                if isfile(_path):
                    return _path
            except:
                return None
        return None

    def _get_path(self, paths):
        '''
        select a valid path from available path list
        '''
        for _path in paths:
            if isdir(_path) or isfile(_path) or glob.glob(_path):
                return _path
        return None

    def _join_path(self, base, path):
        return os.path.join(base, path)

    @handle_exception
    def _build_paths(self, path, *args, **kargs):
        '''
        build paths
        '''
        _upper      = self._upper_path(path)
        _pwdpath    = self._join_path(os.getcwd(), path)
        _relpath    = self._join_path(self.root_path, path)
        return (_upper, _pwdpath, _relpath)

    @handle_exception
    def file_path(self, path, *args, **kargs):
        if path is None:
            return None
        (_upper, _pwdpath, _relpath) = self._build_paths(path)
        _path  = self._get_file([path, _pwdpath, _relpath, _upper])
        return _path

    @handle_exception
    def absolute_path(self, path, *args, **kargs):
        '''
        get the absolute path
        '''
        if path is None:
            return None

        (_upper, _pwdpath, _relpath) = self._build_paths(path)
        _abspath    = self._get_path([path, _pwdpath, _relpath, _upper])
        if _abspath == _upper and 'new' in kargs:
            return path
        elif _abspath is None:
            _abspath = _relpath
            os.makedirs(_abspath)
        return _abspath

    @handle_exception
    def append_paths(self, paths):
        '''
        append path
        '''
        return [self.absolute_path(x) for x in paths]
