import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
import seaborn as sns
import numpy as np
import statsmodels as sm
from sklearn.linear_model import LinearRegression
from statsmodels.formula.api import ols



data = pd.read_csv('/Users/ruotianjiang/Downloads/forestfires.csv')

model = ols('area2 ~ X + Y + M + D + FFMC + DMC + DC + ISI + temp + RH + wind + rain', data).fit()
print(model.summary())




data = pd.read_csv('/Users/ruotianjiang/Downloads/forestfires.csv')


sns.pairplot(data,x_vars=['X','Y','M','D','FFMC','DMC','DC','ISI','temp','RH','wind','rain'], y_vars='area2', size=7, aspect=0.8)
plt.show()
# 'ISI','temp','RH','wind','rain',
