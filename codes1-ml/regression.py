
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
from sklearn.linear_model import LinearRegression


def get_data():


    data = pd.read_csv('/Users/ruotianjiang/Downloads/forestfires.csv')


    X_parameter = []
    Y_parameter = []
    for x,y in zip(data['Y'],data['area2']):
        X_parameter.append([float(x)])
        Y_parameter.append(math.log(1+float(y),math.e))

    return X_parameter,Y_parameter





def linear_model_main(X_parameter,Y_parameter):

    regr = LinearRegression()
    regr.fit(X_parameter,Y_parameter)


    # predict_outcome = regr.predict(predict_square_feet)

    predictions = {}

    predictions['intercept'] = regr.intercept_

    predictions['coefficient'] = regr.coef_
    predictions['R square'] = regr.score(X_parameter,Y_parameter)

    # predictions['predict_value'] = predict_outcome

    return predictions


def show_linear_line(X_parameter,Y_parameter):

    regr = LinearRegression()
    regr.fit(X_parameter,Y_parameter)


    plt.scatter(X_parameter,Y_parameter,color = 'blue')


    plt.plot(X_parameter,regr.predict(X_parameter),color = 'red',linewidth = 4)

    plt.title('linear regression')
    plt.xlabel('Y')
    plt.ylabel('area')
    plt.show()

def main():

    X,Y = get_data()


    result = linear_model_main(X,Y)
    for key,value in result.items():
        print ('{0}:{1}'.format(key,value))

    show_linear_line(X,Y)

if __name__ == '__main__':
    main()
