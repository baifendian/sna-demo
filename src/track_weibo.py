#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# 1. track weibo
# 2. recording user id and retweeted time
# 3. stat diffusion rate and depth
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(cur_dir)

weibo = pd.read_json(base_dir + '/data/weibo_detailed.json')
print "Reading Data Done!"
start_weibo_id = 4052323619919213


class TreeNode(object):
    def __init__(self, weiboid):
        self.weibo_id = weiboid
        self.children = []
        self.user_id = ""
        self.datetime = ""

    def add_info(self, uid, created_time):
        self.user_id = uid
        self.datetime = created_time

    def add_children(self, retweeted_weibo_ids, data):
        for i in retweeted_weibo_ids:
            n = TreeNode(i)
            info = data[data["mid"] == i][["user_uid", "created_at"]]
            if info.shape[0] > 0:
                n.add_info(*info.iloc[0, ])
            self.children.append(n)


def track(cur_node):
    if not (cur_node or isinstance(cur_node, TreeNode)):
        print "invalid TreeNode!"
        return
    retweeted = weibo[weibo["retweeted_mid"] == cur_node.weibo_id]
    if retweeted.shape[0] > 0:
        cur_node.add_children(retweeted.mid.tolist(), weibo)
        for child in cur_node.children:
            track(child)


def cruiser(cur_node, cur_lv=0):
    depth = cur_lv + 1
    max_depth = depth
    weibo_by_hour.extend([(c.datetime - root.datetime).total_seconds() / 3600
                          for c in cur_node.children if c.datetime])
    for child in cur_node.children:
        max_depth = max(cruiser(child, cur_lv=depth), depth)
    return max_depth


root = TreeNode(start_weibo_id)
si = weibo[weibo["mid"] == start_weibo_id][["user_uid", "created_at"]]
if si.shape[0] > 0:
    root.add_info(*si.iloc[0, ])
track(root)
print "Tracking Weibo Done!"

weibo_by_hour = []
print "Max Depth of Retweeting:", cruiser(root)
values, base = np.histogram(weibo_by_hour, bins=100)
cumulative = np.cumsum(values)
plt.subplot(1, 2, 1)
plt.plot(base[:-1], cumulative, c='red')
plt.title('Cumulative Diffusion')
plt.ylabel('Number of Retweets')
plt.xlabel('Hours After Source Weibo')
plt.subplot(1, 2, 2)
plt.plot(base[:-1], values, c='orange')
plt.title('Hourly Diffusion')
plt.xlabel('Hours After Source Weibo')
plt.show()
