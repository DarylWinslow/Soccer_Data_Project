# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:37:20 2016

@author: Daryl
"""

from __future__ import print_function

import os
import subprocess

from time import time
from operator import itemgetter
from scipy.stats import randint

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.grid_search import GridSearchCV
from sklearn.grid_search import RandomizedSearchCV
from sklearn.cross_validation import  cross_val_score
from sklearn.ensemble import AdaBoostClassifier

import getdata

def encode_target(df, target_column):
    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod["Target"] = df_mod[target_column].replace(map_to_int)
    return (df_mod, targets)


df = pd.read_csv("last6model.csv", index_col=0)
testdf = pd.read_csv("futuretestmodel.csv")

testdf1 = getdata.select_columns(testdf, ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 'AGS', 'AGA', 'ARC', 
            'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC'])
            
testbigdf = getdata.select_columns(df, ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 'AGS', 'AGA', 'ARC', 
            'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC'])

features = ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 'AGS', 'AGA', 'ARC', 
            'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC']
df, targets = encode_target(df, "FTR")
y = df["Target"]
X = df[features]


dt = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=0.5, n_estimators=50, random_state=None)
dt.fit(X, y)

scores = cross_val_score(dt, X, y, cv=10)

pred = dt.predict(testdf1)

pred1 = pd.DataFrame(data=pred, columns=["Pred"])
newrow = pd.concat([testdf1, pred1], axis=1)

prediction = pd.DataFrame(newrow).to_csv('prediction.csv')














