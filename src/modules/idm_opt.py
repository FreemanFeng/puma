# -*- coding:utf-8 -*-

import json

import os
import time

from SBase import SBase
from handle_exception import handle_exception

class IdmOpt(SBase):
    def __init__(self, *args, **kargs):
        super(IdmOpt, self).__init__()

    @handle_exception
    def idm_opt(self, *args, **kargs):
        '''
        本类的唯一导出接口
        '''
        return self.inner_call(entity = self, *args, **kargs)

    @handle_exception
    def _load(self, data, *args, **kargs):
        '''
        加载闪屏协议模板
        '''
        self.cm.load_yaml('etc/protocol/idm.yml')
        return json.loads(data)

    @handle_exception
    def _get_node(self, data, *args, **kargs):
        '''
        获取需要修改mock数据的节点位置，闪屏服务应该只会改media
        '''
        (name, node) = data
        if type(node) not in (list, dict):
            return None
        if name in node:
            self.logger.info('Got Node %s : %s' %(name, node[name]))
            return node[name]
        if type(node) is list:
            for _item in node:
                _ret = self.idm_opt(get_node=(name, _item))
                if _ret is not None:
                    return _ret
        else:
            for _item in node.values():
                _ret = self.idm_opt(get_node=(name, _item))
                if _ret is not None:
                    return _ret

    @handle_exception
    def _delete(self, data, *args, **kargs):
        '''
        更新闪屏数据, 删除操作
        '''
        (msg, params) = data
        for _key, _val in params.items():
            del(msg[_key])

    @handle_exception
    def _pop(self, data, *args, **kargs):
        '''
        更新闪屏数据, 删除数组栈顶元素
        '''
        (msg, params) = data
        for _key, _val in params.items():
            if type(msg[_key]) is list:
                msg[_key].pop()

    @handle_exception
    def _append(self, data, *args, **kargs):
        '''
        更新闪屏数据, 往数组添加元素
        '''
        (msg, params) = data
        for _key, _val in params.items():
            if type(msg[_key]) is list:
                msg[_key].append(_val)

    @handle_exception
    def _update(self, data, *args, **kargs):
        '''
        更新闪屏数据, 使用新的值
        '''
        (msg, params) = data
        for _key, _val in params.items():
            msg[_key] = _val

    @handle_exception
    def _readidm(self, path, *args, **kargs):
        '''
        读取本地闪屏协议模板
        '''
        _name   = os.path.basename(path)
        _file   = self.absolute_path(path)
        with open(_file, 'rb') as f:
            _data = f.read()
        return _data

    @handle_exception
    def _test(self, path, *args, **kargs):
        '''
        测试专用
        '''
        _items  = list()
        _data   = self.idm_opt(readidm=path)
        _msg    = self.idm_opt(load=_data)
        _name   = self.cm.idm['node']
        return self.idm_opt(get_node=(_name, _msg))
        #_node = self.idm_opt(get_node=(_name, _msg))
        #_node['display_type'] = 'part'
        #self.logger.info(_msg)

if __name__ == '__main__':
    _obj = IdmOpt()
    _path = "data/idm/idm.json"
    _obj.idm_opt(test=_path)
