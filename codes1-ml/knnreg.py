import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import math
import random
from sklearn import neighbors
from sklearn.neighbors import KNeighborsRegressor
import csv
import sklearn
from fractions import Fraction


with open('/Users/ruotianjiang/Downloads/forestfires.csv','rb') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]
del(rows[0])
random.shuffle(rows)
X=[]
for row in rows:
    a=[row[0],row[1],row[8],row[9],row[10]]
    X.append(a)
# X = [row[8:11] for row in rows]
Y = [float(row[13]) for row in rows]


a=int(len(X)*0.7)
x=X[:a-1]
y=Y[:a-1]
x_test = X[a:]
y_test = Y[a:]

k=1
kl=[]
scorel1=[]
scorel2=[]

x = np.array(x)
y = np.array(y)
# print(x.shape)
# print(y.shape)
# x = x.reshape(-1,5)
# x = y.reshape(-1,)
x_test = np.array(x_test)
y_test = np.array(y_test)
# x_test = x_test.reshape(-1,5)
# y_test = y_test.reshape(-1,)
while k <=a-2:
    kl.append(Fraction(1,k))
    knn = sklearn.neighbors.KNeighborsRegressor(n_neighbors=k)
    knn.fit(x,y)
    score1=knn.score(x_test,y_test,sample_weight=None)
    scorel1.append(1-score1)
    score2=knn.score(x,y,sample_weight=None)
    scorel2.append(1-score2)

    k=k+1

plt.figure(figsize=(8,4))
plt.plot(kl,scorel1,"b-",linewidth=1,label="test error")
plt.plot(kl,scorel2,"r-",linewidth=1,label="train error")
plt.xlabel("1/k")
plt.title("k and error")
plt.show()



# X_test = np.array(OutofExpectation)
# clf=knr(n_neighbors=2, weights='distance').fit(X,Y)
# Y_test = clf.predict(X_test)
