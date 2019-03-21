# -*- coding: utf-8 -*-

import numpy as np
from sklearn.model_selection import train_test_split
# from sklearn import cross_validation
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
import statsmodels.discrete.discrete_model as sm


from train_data import train_data
from test_data import test_data
from diii import get_feature


# change the l value here

index=[1,3,4,5,8,10,11,16]
x, y_train = train_data(3)
x_train=[]
for i in x:
    x_train.append([i[1],i[3],i[4],i[5],i[8],i[10],i[11],i[16]])
x, y_test = test_data(3)
x_test=[]
for i in x:
    x_test.append([i[1],i[3],i[4],i[5],i[8],i[10],i[11],i[16]])
X_train=np.array(x_train)
y_train=np.array(y_train)
X_test=np.array(x_test)
y_test=np.array(y_test)




clf = LogisticRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
p = np.mean(y_pred == y_test)
print("precision:")
print(p)
