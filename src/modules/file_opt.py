# -*- coding:utf-8 -*-
'''
This Class is to register plugins
'''
import os
import re
import glob
from singleton import Singleton
from binding import Binding
from handle_exception import handle_exception

class FileOpt(Singleton):
    '''
    FileOpt Attributes
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize plugin instance
        '''
        super(FileOpt, self).__init__()

        self._content   = list()

        _modules = {
                'inner_call'    :   'InnerCall',
                'convert'       :   'Convert',
                'paths'         :   'Paths'
                }

        Binding().binding(self, modules = _modules, entity = self)

    @handle_exception
    def file_opt(self, *args, **kargs):
        '''
        unique interface for file operation
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _read(self, path, *args, **kargs):
        '''
        read file content
        '''
        _file = self.absolute_path(path)
        with open(_file) as f:
            self._content = [x.strip() for x in f]
            return self._content

    @handle_exception
    def _read_binary(self, path, *args, **kargs):
        '''
        read file content
        '''
        _file = self.absolute_path(path)
        with open(_file) as f:
            return f.read()

    @handle_exception
    def _search_file(self, data, *args, **kargs):
        (path, pattern) = data
        _files = self.convert(join=(path, '/*'))
        _out = list()
        for _file in glob.glob(_files):
            _name = os.path.basename(_file)
            _parts = _name.split(pattern)
            if len(_parts) > 1:
                _out.append(_file)
        return _out

    @handle_exception
    def _read_file(self, config, *args, **kargs):
        '''
        binding modules class methods
        '''
        if 'file' in config:
            _file   = self.absolute_path(config['file'])
            _column = config['column'] if 'column' in config else None
            _split  = config['split'] if 'split' in config else ' '
            with open(_file) as f:
                if _column is None:
                    self._content = [x.strip() for x in f]
                else:
                    self._content = [x.strip().split(_split)[_column] for x in f]
                return self._content

    @handle_exception
    def _get_content(self, *args, **kargs):
        '''
        file content
        '''
        return self._content

    @handle_exception
    def _set_content(self, data, *args, **kargs):
        '''
        set file content to be written
        '''
        self._content = data

    @handle_exception
    def _update_content(self, config, *args, **kargs):
        '''
        update file content to be written
        '''
        if self._content:
            _data   = config['data'] if 'data' in config else None
            _key    = config['key'] if 'key' in config else None
            _index  = config['index'] if 'index' in config else None
            _del    = 1 if 'delete' in config else None

            if _del and _index:
                 self._content[_index] = str()
            elif _index:
                self._content[_index] = data
            elif _key:
                _regexp = re.compile(_key)
                for _id, _item in enumerate(self._content):
                    if _regexp.match(_item):
                        self._content[_id] = _regexp.sub(_item, _data)

    @handle_exception
    def _write_binary(self, data, *args, **kargs):
        '''
        save data
        '''
        (path, content) = data
        with open(path, 'wb') as f:
            f.write(content)

    @handle_exception
    def _write_text(self, data, *args, **kargs):
        '''
        save data
        '''
        (path, content) = data
        with open(path, 'wt') as f:
            f.writelines(content)

    @handle_exception
    def _save(self, path, *args, **kargs):
        '''
        save content
        '''
        return self.file_opt(write_text=(path, self._content))

    @handle_exception
    def _write_file(self, config, *args, **kargs):
        '''
        write file
        '''
        if 'file' in config:
            _file   = config['file']
            self._write(_file)

if __name__ == '__main__':
    _obj = FileOpt()
    _out = _obj.file_opt(search_file=('/home/share/codes/puma/data/cms', 'android_223'))
    print _out
