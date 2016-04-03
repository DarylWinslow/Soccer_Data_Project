# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 12:52:03 2016

@author: Daryl
"""

from __future__ import print_function

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import  cross_val_score

def encode_target(df, target_column):
    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod["Target"] = df_mod[target_column].replace(map_to_int)
    return (df_mod, targets)
    
    
if __name__ == "__main__":
    df = pd.read_csv("last6data.csv", index_col=0)
    
    features = ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 'AGS', 'AGA', 'ARC', 
                'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC']
                
    df, targets = encode_target(df, "FTR")
    y = df["Target"]
    X = df[features]
    
    dt = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
              learning_rate=0.5, n_estimators=50, random_state=None)
    dt.fit(X, y)
    
    scores = cross_val_score(dt, X, y, cv=10)