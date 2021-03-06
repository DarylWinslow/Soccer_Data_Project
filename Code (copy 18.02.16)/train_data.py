import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics as skm
 
dta_fapl2012_2013 = pd.read_csv('E0 (12-13).csv', parse_dates=[1])
dta_fapl2013_2014 = pd.read_csv('E0 (13-14).csv', parse_dates=[1])
 
dta = pd.concat([dta_fapl2012_2013, dta_fapl2013_2014], axis=0, ignore_index=True)
 
#Find the row numbers that should be used for training and testing.
train_idx = np.array(dta.Date < '2014-01-01')
test_idx = np.array(dta.Date >= '2014-01-01')
 
#Arrays where the match results are stored in
results_train = np.array(dta.FTR[train_idx])
results_test = np.array(dta.FTR[test_idx])

feature_columns = ['B365H', 'B365D', 'B365A', 'BWH', 'BWD']

#Column numbers for odds for the three outcomes 
cidx_home = [i for i, col in enumerate(dta.columns) if col[-1] in 'H' and col in feature_columns]
cidx_draw = [i for i, col in enumerate(dta.columns) if col[-1] in 'D' and col in feature_columns]
cidx_away = [i for i, col in enumerate(dta.columns) if col[-1] in 'A' and col in feature_columns]
 
#The three feature matrices for training
feature_train_home = dta.ix[train_idx, cidx_home].as_matrix()
feature_train_draw = dta.ix[train_idx, cidx_draw].as_matrix()
feature_train_away = dta.ix[train_idx, cidx_away].as_matrix()
 
#The three feature matrices for testing
feature_test_home = dta.ix[test_idx, cidx_home].as_matrix()
feature_test_draw = dta.ix[test_idx, cidx_draw].as_matrix()
feature_test_away = dta.ix[test_idx, cidx_away].as_matrix()
 
train_arrays = [feature_train_home, feature_train_draw,
                feature_train_away]
                                     
test_arrays = [feature_test_home, feature_test_draw,
                feature_test_away]
 
imputed_training_matrices = []
imputed_test_matrices = []
 
for idx, farray in enumerate(train_arrays):
    imp = Imputer(strategy='mean', axis=1) #0: column, 1:rows
    farray = imp.fit_transform(farray)
    test_arrays[idx] = imp.fit_transform(test_arrays[idx])
     
    imputed_training_matrices.append(farray)
    imputed_test_matrices.append(test_arrays[idx])
 
#merge the imputed arrays
feature_train = np.concatenate(imputed_training_matrices, axis=1)
feature_test = np.concatenate(imputed_test_matrices, axis=1)

adb = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=3),
    n_estimators=1000,
    learning_rate=0.4, random_state=42)
 
adb = adb.fit(feature_train, results_train)

training_pred = adb.predict(feature_train)
print skm.confusion_matrix(list(training_pred), list(results_train))

test_pred = adb.predict(feature_test)
print skm.confusion_matrix(list(test_pred), list(results_test)) 
