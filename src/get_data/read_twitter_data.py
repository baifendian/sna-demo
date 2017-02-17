#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import os

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
base_dir = os.path.dirname(os.path.dirname(cur_dir))

df = pd.read_excel(base_dir + '/data/Twitter Data Schema.xlsx', sheetname=3, na_values='NULL')


def num2str(num):
    if np.isnan(num):
        return None
    else:
        return str(int(num))


def find_userid(refid):
    if refid:
        uid = df[df["postexternalId"] == refid]["postprofileid"].unique()
        if uid.shape[0] > 0:
            return str(uid[0])
        else:
            return ""
    else:
        return ""

twitter = pd.DataFrame()
twitter["userid"] = df["postprofileid"].apply(str)
twitter["postid"] = df["postexternalId"].apply(num2str)
twitter["refpid"] = df["postreferencedexternalId"].apply(num2str)
twitter["srcuid"] = df["postreferencedexternalId"].apply(find_userid)
# print twitter.head()

data = twitter.groupby(["userid", "srcuid"]).size()
stat = data.reset_index(level=["userid", "srcuid"])
stat.columns = ["to", "from", "weight"]
print stat.head()
stat.to_json(base_dir + "/data/twitter.json", orient="records")
