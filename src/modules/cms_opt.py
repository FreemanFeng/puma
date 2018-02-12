# -*- coding:utf-8 -*-

import json
import os
import time

from SBase import SBase
from binding import Binding
from handle_exception import handle_exception

class CmsOpt(SBase):
    def __init__(self, *args, **kargs):
        super(CmsOpt, self).__init__()

        self._callback = {
                'int' : self._fill_invalid_int
                }

        self._listtype = {
                'checkbox': 1
                }
        self._dicttype = {
                'object': 1
                }

        _modules = {
                'http_opt' : 'HttpOpt'
                }

        Binding().binding(self, modules = _modules, entity = self)
        self.cm.load_yaml('etc/protocol/cms.yml')

    @handle_exception
    def cms_opt(self, *args, **kargs):
        '''
        本类的唯一导出接口
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _fill_invalid_int(self, item, *args, **kargs):
        '''
        设置int类型的非法值
        '''
        item.append("-1")

    @handle_exception
    def _fill_invalid(self, data, *args, **kargs):
        '''
        设置CMS资源模板中特定类型字段的非法值
        '''
        (item, msg) = data
        if msg['type'] in self._callback:
            _type = msg['type']
            _item['invalid'] = list()
            self._callback[_type](item['invalid'])

    @handle_exception
    def _set_list(self, data, *args, **kargs):
        '''
        设置checkbox类型字段，其对应的原始json数据类型为列表
        '''
        (item, msg) = data
        if msg['type'] in self._listtype:
            item['islist'] = 1

    @handle_exception
    def _fill_valid(self, data, *args, **kargs):
        '''
        提取CMS资源模板中checkbox/select类型的可选值
        '''
        (item, msg) = data
        if 'regular' not in msg:
            return
        if type(msg['regular']) is dict:
            self.cms_opt(set_list=(item, msg))
            item['valid'] = list()
            _valid = item['valid']
            for _key in msg['regular']:
                _valid.append(_key)

    @handle_exception
    def _fill_default(self, data, *args, **kargs):
        '''
        提取CMS资源模板中各字段的默认值
        '''
        (item, key, msg) = data
        item[key] = str()
        if key in msg:
            item[key] = msg[key]

    @handle_exception
    def _fill(self, data, *args, **kargs):
        '''
        通过CMS资源模板，提取原始json字段以及对应的默认值、可选值
        '''
        (items, key, msg) = data
        _item = dict()
        _name = self.cm.cms['node']
        _node = msg[key]
        #+=======================
        #| 嵌套object类型定义
        #+=======================
        if _node['type'] in self._dicttype and _name in _node:
            _subitems = list()
            _def = _node[_name]
            for _k, _v in _def.items():
                self.cms_opt(fill=(_subitems, _k, _def))
            _item['key'] = key
            _item['data'] = _subitems
            _item['isdict'] = 1
            items.append(_item)
            return
        #+=======================
        #| 普通的定义
        #+=======================
        self.cms_opt(fill_default=(_item, 'default', msg[key]))
        self.cms_opt(fill_valid=(_item, msg[key]))
        _item['key'] = key
        items.append(_item)

    @handle_exception
    def _delete(self, data, *args, **kargs):
        '''
        更新原始json数据, 删除操作
        '''
        (msg, params) = data
        for _key, _val in params.items():
            del(msg[_key])

    @handle_exception
    def _pop(self, data, *args, **kargs):
        '''
        更新原始json数据, 删除数组栈顶元素
        '''
        (msg, params) = data
        for _key, _val in params.items():
            if type(msg[_key]) is list:
                msg[_key].pop()

    @handle_exception
    def _append(self, data, *args, **kargs):
        '''
        更新原始json数据, 选取可选值
        '''
        (msg, items, params) = data
        for _key, _val in params.items():
            if type(msg[_key]) is not list:
                continue
            for _item in items:
                if _item['key'] != _key:
                    continue
                if self.convert(isnum=_val) is None:
                    msg[_key].append(_val)
                    continue
                _pos    = int(_val)
                _valid  = _item['valid']
                _data   = _valid[_pos]
                msg[_key].append(_data)

    @handle_exception
    def _select(self, data, *args, **kargs):
        '''
        更新原始json数据, 选取可选值
        '''
        (msg, items, params) = data
        for _key, _val in params.items():
            if type(msg[_key]) is not list:
                continue
            for _item in items:
                if _item['key'] != _key:
                    continue
                if self.convert(isnum=_val) is None:
                    msg[_key] = list()
                    msg[_key].append(_val)
                    continue
                _pos    = int(_val)
                _valid  = _item['valid']
                _data   = _valid[_pos]
                msg[_key] = list()
                msg[_key].append(_data)

    @handle_exception
    def _update(self, data, *args, **kargs):
        '''
        更新原始json数据, 使用新的值
        '''
        (msg, params) = data
        for _key, _val in params.items():
            msg[_key] = _val


    @handle_exception
    def _build_msg(self, data, *args, **kargs):
        '''
        使用默认值填充原始json数据,
        如果是数组类型(checkbox)，选取第一个元素
        如果是字典类型(object)，递归创建结构体
        '''
        (item, msg) = data
        _name = item['key']
        if 'islist' in item:
            msg[_name] = list()
        elif 'isdict' in item:
            msg[_name] = dict()
            for _subitem in item['data']:
                self.cms_opt(build_msg=(_subitem, msg[_name]))
        else:
            msg[_name] = str()
        _node = msg[_name]
        if 'valid' in item:
            _valid = item['valid']
            if type(_node) is list:
                if 'islist' in item:     #TODO checkbox type, select all value
                    _node.extend(_valid)
                else:
                    _node.append(_valid[0])
            else:
                msg[_name] = _valid[0]
        elif 'default' in item:
            msg[_name] = item['default']

    @handle_exception
    def _getres(self, output, *args, **kargs):
        '''
        获取资源模板，保存到本地为json文件
        '''
        _config = dict()
        _api = self.cm.cms['api']
        _node = _api['getres']
        _config['url'] = self.convert(join=(_api['host'], _api['ver'], _node['path']))
        _resp = self.get_url(_config)
        _data = json.loads(_resp.text)
        if type(_data) is not dict or _data['status'] != 200:
            self.logger.info('Get CMS Res Failed!')
            return
        for _item in _data['data']:
            _resid      = _item['res_id']
            _entid      = _item['ent_id']
            if _entid > 2:
                continue
            _platform   = _node['platform'][_entid]
            _code       = _item['code']
            _name       = self.convert(underscore=(_platform, _resid, _code))
            _name       = self.convert(dot=(_name, 'json'))
            _path       = self.absolute_path(output)
            _file       = os.path.join(_path, _name)
            if len(_item['data_format']) == 0:
                continue
            _format = json.loads(_item['data_format'])
            with open(_file, 'w+') as f:
                json.dump(_format, f, indent=4, separators=(',', ': '))

    @handle_exception
    def _pushcms(self, data, *args, **kargs):
        '''
        将原始json数据push到CMS后台接口，由CMS后台打包成资源
        data_type为2时推荐临时数据，为1时默认数据
        '''
        (resid, msg, cond, datatype) = data
        _config = dict()
        _api = self.cm.cms['api']
        _node = _api['pushcms']
        _config['url'] = self.convert(join=(_api['host'], _api['ver'], _node['path']))
        _body = dict()
        _body['res_id'] = str(resid)
        _body['cond'] = dict()
        if cond is None and _node['cond'] is None:
            _body['cond'] = dict()
        elif cond is None:
            _body['cond'].update(_node['cond'])
        elif type(cond) is dict:
            _body['cond'].update({x:str(y) for x, y in cond.items()})
        _body['data_type'] = str(datatype)
        _data = list()
        _data.append(msg)
        _body['data'] = json.dumps(_data)
        _config['json'] = _body
        self.logger.info('body %s' % _body)
        self.logger.info(_config['json'])
        self.http_opt(post_json=_config)

    @handle_exception
    def _load(self, data, *args, **kargs):
        '''
        加载CMS资源模板，生成原始json数据
        '''
        _defs = json.loads(data)
        _name = self.cm.cms['node']
        _node = _defs[_name]
        _items = list()
        for _key in _node:
            self.cms_opt(fill=(_items, _key, _node))
        _msg = dict()
        for _item in _items:
            self.cms_opt(build_msg=(_item, _msg))
        return (_msg, _items)

    @handle_exception
    def _readcms(self, path, *args, **kargs):
        '''
        读取本地资源模板的文件，提取ent_id，res_id以及资源模板内容
        '''
        _name   = os.path.basename(path)
        _parts  = _name.split('_')
        _entid  = _parts[0]
        _resid  = _parts[1]
        _file   = self.absolute_path(path)
        with open(_file, 'rb') as f:
            _data = f.read()
        return (_entid, _resid, _data)

    @handle_exception
    def _searchcms(self, data, *args, **kargs):
        (platform, resid, path) = data
        _prefix = self.convert(join=(platform, '_', resid))
        self.logger.info('Searching File matched %s in %s' % (_prefix, path))
        _out = self.file_opt(search_file=(path, _prefix))
        return _out[0]

    @handle_exception
    def _test(self, path, *args, **kargs):
        '''
        测试专用
        '''
        self.cms_opt(init=1)
        self.cms_opt(getres=path)

if __name__ == '__main__':
    _obj = CmsOpt()
    _path = "testing/ucstart/data/cms"
    _obj.cms_opt(test=_path)
