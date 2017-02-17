#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import networkx as nx
import os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(cur_dir)

sn = nx.read_gpickle(base_dir + "/data/weibo.gpickle")

usn = sn.to_undirected()
# largest connected components of this graph
lcc = max(nx.connected_component_subgraphs(usn), key=len)
eccen = nx.eccentricity(lcc)    # 节点离心度
print eccen['1645005104']       # 得到节点离心度，其中为源微博用户的节点离心度
# out: 9

# 找到扩散尝试最大的节点
path_length = nx.all_pairs_shortest_path_length(sn)
src_path = path_length['1645005104']
max_depth = filter(lambda x: src_path[x] == max(src_path.values()), src_path.keys())
print len(max_depth)
# out: 52
