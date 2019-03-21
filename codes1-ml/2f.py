import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import math
from sklearn.model_selection import train_test_split

plt.figure()
plt.title('single variable')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

def get_data():


    data = pd.read_csv('/Users/ruotianjiang/Downloads/forestfires.csv')


    X_parameter = []
    Y_parameter = []
    for x,y in zip(data['DMC'],data['area']):
        X_parameter.append([float(x)])
        Y_parameter.append(math.log(1+float(y),math.e))

    return X_parameter,Y_parameter

X,Y = get_data()
x , x_test , y,y_test = train_test_split(X,Y,test_size=0.3 ,random_state=0)
# x=X[:400]
# y=Y[:400]
# x_test = X[401:]
# y_test = Y[401:]
plt.plot(x, y, 'g.',markersize =8)


model = LinearRegression()
x2 = [[0], [300]]
model.fit(x, y)
y2 = model.predict(x2)
plt.plot(x2, y2,label = '$y = ax + c$')
plt.legend()


xx = np.linspace(0, 300, 300)
quadratic_featurizer = PolynomialFeatures(degree = 2)
x_train_quadratic = quadratic_featurizer.fit_transform(x)
xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1))

regressor_quadratic = LinearRegression()
regressor_quadratic.fit(x_train_quadratic, y)
plt.plot(xx, regressor_quadratic.predict(xx_quadratic),label="$y = ax^2 + bx + c$")
plt.legend()

cubic_featurizer = PolynomialFeatures(degree = 3)
x_train_cubic = cubic_featurizer.fit_transform(x)
xx_cubie = cubic_featurizer.transform(xx.reshape(xx.shape[0], 1))

regressor_cubic = LinearRegression()
regressor_cubic.fit(x_train_cubic, y)
plt.plot(xx, regressor_cubic.predict(xx_cubie),label="$y = a_1x^3 + a_2x^2 + a_3x +c $")
plt.legend()

print '1 r-squared', model.score(x_test, y_test)
x_test_quadratic = quadratic_featurizer.transform(x_test)
print '2 r-squared', regressor_quadratic.score(x_test_quadratic, y_test)
x_test_cubic = cubic_featurizer.transform(x_test)
print '3 r-squared', regressor_cubic.score(x_test_cubic, y_test)
plt.show()