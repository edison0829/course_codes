# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn import feature_selection as fs
import statsmodels.discrete.discrete_model as sm


from train_data import train_data
from test_data import test_data
from diii import get_feature

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


y_true=y_test
y_pred=clf.predict(X_test)
y_hat = clf.predict_proba(X_test)[:,1]

y_hat=np.ravel(y_hat)

fprs, tprs, thresholds = metrics.roc_curve(y_true, y_hat)


plt.plot(fprs, tprs, 'k--', lw=2)
plt.scatter(fprs, tprs, c='k', marker='x', s=50)
plt.plot(np.arange(-.05, 1.05, .01), np.arange(-.05, 1.05, .01), '--', color='lightgray')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.xlim([0-.05, 1+.05])
plt.ylim([0-.05, 1+.05])
plt.show()
print(metrics.roc_auc_score(y_test, y_hat))
print(metrics.confusion_matrix(y_true, y_pred))
res=sm.Logit(y_train,X_train).fit(method='bfgs')
print(res.summary())
