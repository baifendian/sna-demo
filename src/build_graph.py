#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(cur_dir)

sn = nx.DiGraph()
data = pd.read_json(base_dir + '/data/twitter.json')

for _, fr, to, w in data.itertuples():
    if to:
        sn.add_edge(fr, to, weight=w)
    else:
        sn.add_node(fr)


nx.draw(sn)
plt.show()
