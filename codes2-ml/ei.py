# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
import statsmodels.discrete.discrete_model as sm
from sklearn import feature_selection as fs
from sklearn.model_selection import StratifiedKFold
from train_data import train_data


# change the l value here

for c in range(1,51):
    m=0
    precision=[]
    for n in range(1,11):
        x_train, y_train = train_data(n)

        x_train=np.array(x_train)
        y_train=np.array(y_train)

        kf=StratifiedKFold(n_splits=5,shuffle=True)

        # y_train=np.ravel(y_train)
        # res=sm.Logit(y_train,x_train).fit(method='bfgs')
        # print(res.summary())


        score=0

        for train_index, test_index in kf.split(x_train,y_train):
            X_train1, X_test1 = x_train[train_index], x_train[test_index]
            y_train1, y_test1 = y_train[train_index], y_train[test_index]
            clf = LogisticRegression(penalty='l1',C=c)
            clf.fit(X_train1, y_train1)
            score = score + clf.score(X_test1,y_test1)
        precision.append(score/5.000000000000)
    p = max(precision)
    if p > m:
        m = p
        value = c
        l=precision
print("precision:")
print m
print("c:")
print c
print("list:")
print l
