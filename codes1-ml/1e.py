from sklearn import neighbors
from sklearn.neighbors import KNeighborsClassifier
from read import DataUtils
import datetime
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def main():
    trainfile_X = '/Users/ruotianjiang/Downloads/train-images-idx3-ubyte'
    trainfile_y = '/Users/ruotianjiang/Downloads/train-labels-idx1-ubyte'
    testfile_X = '/Users/ruotianjiang/Downloads/t10k-images-idx3-ubyte'
    testfile_y = '/Users/ruotianjiang/Downloads/t10k-labels-idx1-ubyte'

    train_X = DataUtils(filename=trainfile_X).getImage()
    train_y = DataUtils(filename=trainfile_y).getLabel()
    test_X = DataUtils(testfile_X).getImage()
    test_y = DataUtils(testfile_y).getLabel()

    return train_X[:5001], train_y[:5001], test_X, test_y


def testKNN():
    train_X, train_y, test_X, test_y = main()



    score2l=[]
    i=0.1
    while i<=1:
        knn = KNeighborsClassifier(n_neighbors=4,p=10**i)
        knn.fit(train_X, train_y)
        score2=knn.score(test_X,test_y,sample_weight=None)
        score2l.append(1-score2)
        i=i+0.1
    print(score2l)



    # print 'Accuracy:',score1
    # print 'Accuracy:',score2



    # startTime = datetime.datetime.now()
    # knn = neighbors.KNeighborsClassifier(n_neighbors=3)
    # knn.fit(train_X, train_y)
    # match = 0;
    # for i in xrange(len(test_y)):
    #     predictLabel = knn.predict(test_X[i])[0]
    #     if(predictLabel==test_y[i]):
    #         match += 1
    #
    # endTime = datetime.datetime.now()
    # print 'use time: '+str(endTime-startTime)
    # print 'error rate: '+ str(1-(match*1.0/len(test_y)))

if __name__ == "__main__":
    testKNN()
