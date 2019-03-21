# -*- coding: utf-8 -*-
# from matplotlib import pyplot
# import scipy as sp
import numpy as np
from sklearn.model_selection import train_test_split
# from sklearn import cross_validation
from sklearn import datasets
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
import statsmodels.discrete.discrete_model as sm
from sklearn import feature_selection as fs
from sklearn.model_selection import StratifiedKFold

from train_data import train_data
# from test_data import test_data
# method='bfgs'

# change the l value here
def get_feature(n):
    x_train, y_train = train_data(n)
    # x_test, y_test = te4t_data()
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    # x_test=np.array(x_test)
    # y_test=np.array(y_test)

    kf=StratifiedKFold(n_splits=5,shuffle=True)
    p=0
    # y_train=np.ravel(y_train)
    # res=sm.Logit(y_train,x_train).fit(method='bfgs')
    # print(res.summary())
    a=[]
    for train_index, test_index in kf.split(x_train,y_train):
        X_train1, X_test1 = x_train[train_index], x_train[test_index]
        y_train1, y_test1 = y_train[train_index], y_train[test_index]
        select_feature=fs.SelectFwe()
        select_feature.fit(X_train1, y_train1)
        print(select_feature.get_support(True))
        #  get new X arrary
        X_train1 = select_feature.transform(X_train1)
        X_test1 = select_feature.transform(X_test1)


        # y_train=np.ravel(y_train)

        clf = LogisticRegression()
        clf.fit(X_train1, y_train1)
        y_pred = clf.predict(X_test1)
        a.append(np.mean(y_pred == y_test1))
        p = p + np.mean(y_pred == y_test1)

    print(a)
    print("precision:")
    print(p/5.000000000000)
    return select_feature
if __name__ == "__main__":
    get_feature(10)
