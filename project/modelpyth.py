import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

data1 = pd.read_excel('E:/Minor Project/project/Final Data.xlsx')

data=pd.DataFrame({
        'ball-bearing': data1['ball-bearing'],
        'vibration': data1['vibration'],
        'condition': data1['condition']
    })

def model_variablereturn():
    X=data[['ball-bearing', 'vibration']]
    y=data['condition']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    ##clf=RandomForestClassifier(n_estimators=4)
    clf=RandomForestClassifier(
    max_depth= 3, min_samples_leaf=1,
    min_samples_split=2,n_estimators=20, n_jobs=1)
    clf.fit(X_train,y_train)
    return clf
