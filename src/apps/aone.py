# -*- coding: utf-8 -*-
'''
This is the Access Library for Aone
'''
#第一步：引入依赖包、定义公共参数：

#引入依赖包
import urllib, httplib, urllib2
import json
import time
import os, sys, datetime
from Crypto.Cipher import AES

#定义公共参数
debug = False
appname = 'uc-feedback-system'  #aone app

if debug:
    url = "http://daily-workitem.aone.alibaba.net/"
    host = 'ak-api.taobao.net'
    secret = 'lTi7skE3u2lwc6gcgdi9Ew=='
    parentId = 1
else:
    parentId = 1
    host = 'aone-api.alibaba-inc.com'
    secret = 'RNe1E1p6s474BMRsMIww0g=='

#第二步：封装AES，完成签名加密

#封装AECS
class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_ECB #切记必须用MODE_ECB模式
        self.BS = AES.block_size
        #补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s : s[0:-ord(s[-1])]

    def encrypt(self,text):
        text = self.pad(text)
        cryptor = AES.new(self.key,self.mode, b'0000000000000000') #必须16位
        ciphertext = cryptor.encrypt(text)
        return ciphertext
#签名计算
def sign(timestamp):
    import base64
    print 'secret:', secret
    content = format("appName=%s;timestamp=%s" % (appname, timestamp));
    key = base64.decodestring(secret)
    print 'key:', key
    ciphertext = prpcrypt(key).encrypt(content.encode('utf-8')) #utf8编码
    return base64.urlsafe_b64encode(ciphertext).rstrip('=') #必须urlsafe格式后，tstrip掉"="


#第三步：封装http请求方法

def sendhttp(url, params):
    timestamp = int(time.time() * 1000)
    signature = sign(timestamp)
    headers = {}
    headers["clientKey"] = appname
    headers["timestamp"] = long(timestamp) #确保长整型
    headers["signature"] = signature
    headers["Content-Type"] = 'application/x-www-form-urlencoded'  #必须显式指定"Content-Type"为'application/x-www-form-urlencoded'

    data = urllib.urlencode(params)
    conn = httplib.HTTPConnection(host)

    print'method:'
    print url
    print'data:'
    print data
    print'headers:'
    print headers
    conn.request('POST', url, data, headers)
    httpres = conn.getresponse()

    result = httpres.read()
    print'response:'
    print result
    try:
        return json.loads(result)['result']
    except:
        import traceback
        traceback.print_exc()


#第四步：接口调动

#以创建项目为例

def createProject(name, description):
    mode = 'public'  #私有 or 共有
    stamp = 'research' #研发空间 or 业务空间
    members = {"ak.akproject.admin":["adminId"]}  #管理员员工号
    url = "/project/openapi/ProjectApiFacade/newProject"  #被调用接口

    params = {}
    params['parentId'] = parentId
    params['mode'] = mode
    params['stamp'] = stamp
    params['members'] = members
    params['name'] = name
    params['description'] = description

    data = {'paramJson': json.dumps(params),
            'staffId': 'xxxxx',  #创建人工号
            'region': "alibaba"  #租户信息：集团 -- alibaba
            }  #data中参数必须小驼峰标志

    return sendhttp(url, data)

if __name__ == '__main__':
    timestamp = int(time.time() * 1000)
    timestamp = 1512373306426
    print timestamp
    signature = sign(timestamp)
    print signature
    url = "/issue/openapi/IssueTopService/create"
