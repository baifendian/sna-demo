#!/usr/bin/evn python
# -*- coding:utf-8 -*-
from datetime import datetime
import requests
import json
import time
import os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(os.path.dirname(cur_dir))


def get_token():
    invalid = True
    token = dict()
    try:
        token = json.load(open("token.json", "r"))
        expire = datetime.strptime(token["exprise"], "%Y-%m-%d %H:%M:%S")
        if expire > datetime.now():
            invalid = False
    except Exception as e:
        print e.message
    if invalid:
        url = "http://sm.viewslive.cn/api1.2/authorize"
        req = {
               "appid": 23090,
               "appkey": "CfJObHSGLa9p7HMpBsbq",
               "username": "baifendian",
               "password": "bfd123"
        }
        r = requests.post(url, data=req)
        with open("token.json", "w") as f:
            f.write(r.text)
        token = json.loads(r.text)
    return token["token"]


def get_idkey(apptoken):
    try:
        tasks = json.load(open("idkey.json", "r"))
    except Exception as e:
        print e.message
        url = "http://sm.viewslive.cn/api1.2/task/list?token=%s" % apptoken
        r = requests.post(url)
        tasks = r.json()
    json.dump(tasks, open("idkey.json", "w"))
    task_detail = tasks["data"]
    if len(task_detail) > 0:
        return task_detail[0]["idkey"]


def get_result():
    url = "http://sm.viewslive.cn/api1.2/task/result"
    req = {
        ""
    }
    r = requests.post(url, data=req)
    return json.loads(r.text)


def get_stream(apptoken, idkey, startid=1):
    url = "http://sm.viewslive.cn/api1.2/task/stream"
    req = {
        "token": apptoken,
        "idkey": idkey,
        "count": 500,
        "startid": startid
    }
    r = requests.post(url, data=req)
    return r.json()

pagesize = 500
tk = get_token()
key = get_idkey(tk)

weibo = []
cur = 380001    # current id of records
flag = True
start = time.clock()
while flag:
    try:
        data = get_stream(tk, key, startid=cur)
        # append data together
        weibo.extend(data["data"])
        # the results count is less than 500 when reaching the tail records.
        if data["count"] < pagesize:
            cur += data["count"]
            flag = False
        else:
            cur += pagesize
    except Exception as err:
        print err.message
        flag = False
    if len(weibo) >= 10000 or (not flag):
        print "dumping records up to %d" % (cur - 1)
        fn = base_dir + "/data/weibo_end_%d.json" % (cur - 1)
        json.dump(weibo, open(fn, "w"))
        weibo = []

end = time.clock()
print 'Time Usage: %.6fs' % (end - start)
print 'Total Records: %d' % (cur - 1)
# 16min, 28w, 560requests
# 4min, 9w,
# 12.763447s, 8390, 20requests
