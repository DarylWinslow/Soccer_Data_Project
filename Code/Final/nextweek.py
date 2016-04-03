# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:37:20 2016

@author: Daryl
"""

from __future__ import print_function

import pandas as pd
import getdata
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import  cross_val_score

def encode_target(df, target_column):
    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod["Target"] = df_mod[target_column].replace(map_to_int)
    return (df_mod, targets)
    
def decode_target(olddf):
    newdf= pd.DataFrame(columns=['Date', 'HomeTeam', 'AwayTeam', 'Prediction',])    
    
    for index, row in olddf.iterrows():
        date=row['Date']
        home=row['HomeTeam']
        away=row['AwayTeam']        
        predint = row['Pred']
        if predint == 0:
            predchar = 'A'
        elif predint == 1:
            predchar = 'D'
        elif predint == 2:
            predchar = 'H'
        d = {'Date': [date], 'HomeTeam': [home], 'AwayTeam': [away], 'Prediction': [predchar]}
        df = pd.DataFrame(d, columns=['Date', 'HomeTeam', 'AwayTeam', 'Prediction'])  
        newdf = newdf.append(df)     
    return (newdf)


if __name__ == "__main__":
    fixtures = "./fixtures/matchweek34.csv"
    
    df = pd.read_csv("last6data.csv", index_col=0)
    
    nextgamesdf = pd.read_csv(fixtures)
    
    modeldf = getdata.create_model_data(nextgamesdf)
    
    features = ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 'AGS', 'AGA', 'ARC', 
                'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC']
                
    df, targets = encode_target(df, "FTR")
    y = df["Target"]
    X = df[features]
    
    dt = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
              learning_rate=0.5, n_estimators=50, random_state=None)
    dt.fit(X, y)
    
    scores = cross_val_score(dt, X, y, cv=10)
    
    predcols = getdata.select_columns(modeldf, ['HWDL', 'HGS', 'HGA', 'HRC', 'AWDL', 
                                              'AGS', 'AGA', 'ARC', 'H2hWDL', 
                                              'H2hGS', 'H2hGA', 'H2hRC'])
    
    pred = dt.predict(predcols)
    
    preddf = pd.DataFrame(data=pred, columns=["Pred"])
    
    result = decode_target(pd.concat([nextgamesdf, preddf], axis=1))
    
    with open("prediction.csv", 'w') as f:
            result.to_csv(f)












