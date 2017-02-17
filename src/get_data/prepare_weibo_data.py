#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import os
import glob
import time
import pandas as pd

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(os.path.dirname(cur_dir))

# list all the data files
datafiles = glob.glob(base_dir + '/data/weibo_end_*.json')

start = time.clock()
weibo = pd.DataFrame()
weibo_retweeted = pd.DataFrame()
for f in datafiles:
    weibo = weibo.append(pd.read_json(f, orient="records"))
    weibo.drop_duplicates(inplace=True)
    weibo_retweeted = weibo_retweeted.append(weibo[weibo["retweeted_uid"] > 0])
    weibo_retweeted.drop_duplicates(inplace=True)
    # break
end = time.clock()
print "Filtering Data Time Used:", end - start

print weibo.head()
print "weibo total number:", weibo.shape
print "retweeted weibo total number:", weibo_retweeted.shape
start = time.clock()
weibo.to_json(base_dir + "/data/weibo_detailed.json", orient="records")
weibo_retweeted.to_json(base_dir + "/data/weibo_retweeted.json", orient="records")

data = weibo_retweeted[["user_uid", "retweeted_uid"]]
data = data.groupby(["user_uid", "retweeted_uid"]).size()
stat = data.reset_index(level=["user_uid", "retweeted_uid"])
stat.columns = ["to", "from", "weight"]
stat.to_json(base_dir + "/data/weibo.json", orient="records")
end = time.clock()
print "Dumping Data Time Used:", end - start
