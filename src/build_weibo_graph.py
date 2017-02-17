#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(cur_dir)

sn = nx.DiGraph()
data = pd.read_json(base_dir + '/data/weibo.json')

for _, fr, to, w in data.itertuples():
    sn.add_edge(str(fr), str(to), weight=w)
nx.write_gpickle(sn, base_dir + "/data/weibo.gpickle")

# KOL
d = nx.out_degree_centrality(sn)
out_d = sorted(d, key=d.get, reverse=True)
print out_d[:5]

# 活跃用户
d = nx.in_degree_centrality(sn)
in_d = sorted(d, key=d.get, reverse=True)
print in_d[:5]

# 交际花, two ways of calculation
d = nx.closeness_centrality(sn)
clo_d = sorted(d, key=d.get, reverse=True)
print clo_d[:5]

d = nx.betweenness_centrality(sn)
bet_d = sorted(d, key=d.get, reverse=True)
print bet_d[:5]

degree_hist = nx.degree_histogram(sn)
x = range(len(degree_hist))
y = [i / float(sum(degree_hist)) for i in degree_hist]
plt.loglog(x, y)
plt.show()

# nx.draw(sn)
# plt.show()
