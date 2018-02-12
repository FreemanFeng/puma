# -*- coding:utf-8 -*-
'''
This Class is to convert data
'''
import os
import re
import base64
import md5
import random
#import hashlib
from time import time, strftime, localtime

# C extension
#from ext.md5 import Md5
#from Md5 import Md5Init, Md5Update, Md5Final, MD5_CTX
#from ext.base64 import Base64

from singleton import Singleton
from binding import Binding
from handle_exception import handle_exception

class Convert(Singleton):
    '''
    Class for Converting Data
    Don't use the function name as argument name
    '''
    def __init__(self, *args, **kargs):
        '''
        initialize
        '''
        super(Convert, self).__init__()

        _modules = {
                'inner_call'        :   'InnerCall'
                }

        Binding().binding(self, modules = _modules, entity = self)
        self.convert(*args, **kargs)

    @handle_exception
    def convert(self, *args, **kargs):
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _to_digit(self, data, *args, **kargs):
        if len(data) == 1:
            return ord(data)
        return data

    @handle_exception
    def _now(self, format=None, *args, **kargs):
        '''
        get currrent time
        '''
        if not format:
            return time()
        elif format == 1:
            return strftime('%H%M%S',localtime(time()))
        elif format == 2:
            return strftime('%H%M%S%f',localtime(time()))
        return strftime('%Y-%m-%d %H:%M:%S',localtime(time()))

    @handle_exception
    def _set_attr(self, data, *args, **kargs):
        '''
        Set Attribute
        '''
        (name, value, target) = data

        return target.__setattr__(name, value)

    @handle_exception
    def _clone(self, data, *args, **kargs):
        '''
        Clone Attribute to target entity
        '''
        (name, source, target, cm) = data

        _value = getattr(source, name)

        if not _value:
            _value = getattr(target, name)

        elif not getattr(target, name):
            self._set_attr((name, _value, target))

        elif type(_value) is list:
            _value.extend(getattr(target, name))
            self._set_attr((name, _value, target))

        else:
            _value = getattr(target, name)
        self._set_attr((name, _value, cm))
        return _value

    @handle_exception
    def _bmd5(self, data, *args, **kargs):
        if not data:
            data = self._random(1)
        return md5.md5(data).digest()

    @handle_exception
    def _md5(self, data, *args, **kargs):
        #return hashlib.md5(data).hexdigest()
        return md5.md5(data).hexdigest()

    @handle_exception
    def _enc64(self, data, *args, **kargs):
        return base64.b64encode(data)

    @handle_exception
    def _encb64(self, data, *args, **kargs):
        return base64.b64encode(data, 'XY')

    @handle_exception
    def _decb64(self, data, *args, **kargs):
        return base64.b64decode(data)

    @handle_exception
    def _short(self, data, length=8, *args, **kargs):
        return str(data)[:length]

    @handle_exception
    def _tid(self, data, *args, **kargs):
        _data   = self._bmd5(data)
        _buf    = self._short(_data, length=6)
        return self._encb64(_buf)

    @handle_exception
    def _random(self, seed, *args, **kargs):
        _time   = self._now()
        _int    = random.randint(0, 1000)
        _data   = self._join((_time, _int, seed))
        _md5    = self._md5(_data)
        return self._short(_md5)

    @handle_exception
    def _sign(self, length, *args, **kargs):
        _data   = self._bmd5(self._random(1))
        return self._encb64(_data)[:length]

    @handle_exception
    def _enctext(self, data, *args, **kargs):
        _data   = self._md5(data)
        return self._encb64(_data)[:8]

    @handle_exception
    def _randint(self, max_int, *args, **kargs):
        return random.randint(0, max_int)

    @handle_exception
    def _random_int(self, base, *args, **kargs):
        return base+random.randint(0, base)

    @handle_exception
    def _to_list(self, data, *args, **kargs):
        return data if type(data) is list else [data]

    @handle_exception
    def _to_dict(self, data, *args, **kargs):
        return data if type(data) is dict else {data:None}

    @handle_exception
    def _home(self, *args, **kargs):
        return os.getenv('HOME')

    @handle_exception
    def _path(self, data, *args, **kargs):
        if data.find('~') == 0:
            return self._join_str(self._home(), data[1:])
        return data

    @handle_exception
    def _dict_to_str(self, data, *args, **kargs):
        if type(data) is dict:
            for _key, _value in data.items():
                data[_key] = str(_value)
        return data

    @handle_exception
    def _to_str(self, data, *args, **kargs):
        return [str(x) for x in data]

    @handle_exception
    def _join_str(self, data, *args, **kargs):
        '''
        use build-in join method
        '''

        if type(data) not in (list, tuple):
            return data

        if len(data) < 2:
            return data

        elif type(data[1]) in (list, tuple):
            return data[0].join(self._to_str(data[1]))

        data = self._to_str(data)

        if len(data) == 2:
            return ''.join(data)

        return data[0].join(data[1:])

    @handle_exception
    def _upper_first(self, data, *args, **kargs):
        return self._join_str((data[0].upper(), data[1:]))

    @handle_exception
    def _join(self, data, *args, **kargs):
        return self._join_str(('', data))

    @handle_exception
    def _slash(self, data, *args, **kargs):
        return self._join_str((data, '/'))

    @handle_exception
    def _pipe(self, data, *args, **kargs):
        return self._join_str(('|', data))

    @handle_exception
    def _underscore(self, data, *args, **kargs):
        return self._join_str(('_', data))

    @handle_exception
    def _dot(self, data, *args, **kargs):
        return self._join_str(('.', data))

    @handle_exception
    def _colon(self, data, *args, **kargs):
        return self._join_str((':', data))

    @handle_exception
    def _log(self, data, *args, **kargs):
        return self._join_str(('`', data))

    @handle_exception
    def _params(self, data, *args, **kargs):
        _list   = self.convert(to_str=data)
        _keys   = _list[::2]
        _vals   = _list[1::2]
        _cnt    = len(_keys)
        _parts  = [self.convert(join=(_keys[i], '=', _vals[i])) for i in range(_cnt)]
        return self.convert(join_str=('&', _parts))

    @handle_exception
    def _space(self, data, *args, **kargs):
        _space = ' '
        if 'col' in kargs:
            _space = ' ' * (kargs['col'] - len(str(data[0])))
        return self._join_str((_space, data))

    @handle_exception
    def _newline(self, data, *args, **kargs):
        return self._join_str((data, '\n'))

    @handle_exception
    def _rn(self, data, *args, **kargs):
        return self._join_str((data, '\r\n'))

    @handle_exception
    def _star(self, data, *args, **kargs):
        return self._join_str((data, '*'))

    @handle_exception
    def _karg(self, data, *args, **kargs):
        return self._join_str(('=', data[0], data[1]))

    @handle_exception
    def _args(self, data, *args, **kargs):
        return self._join_str((',', data))

    @handle_exception
    def _isnum(self, data, *args, **kargs):
        return re.match(r'[+-]?\d+$', data)

    @handle_exception
    def _test(self, data, *args, **kargs):
        '''
        测试专用
        '''
        _ret = self.convert(params=('mac', '214353523523', 'imei', 'kkkkkkkkk'))
        print _ret

if __name__ == '__main__':
    _obj = Convert()
    _obj.convert(test=1)
