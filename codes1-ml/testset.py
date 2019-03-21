from sklearn import neighbors
from sklearn.neighbors import KNeighborsClassifier
from read import DataUtils
import datetime
import matplotlib.pyplot as plt
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

    return train_X, train_y, test_X, test_y


def testKNN():
    train_X, train_y, test_X, test_y = main()

    k=3
    numl=[]
    score1l=[]
    num=5000
    while num <= 30000:


        knn = KNeighborsClassifier(n_neighbors=4)
        knn.fit(train_X[:num], train_y[:num])
        score1=knn.score(test_X,test_y,sample_weight=None)
        score1l.append(1-score1)
        numl.append(num)
        num=num+5000


    # print 'Accuracy:',score1
    # print 'Accuracy:',score2
    x = numl
    y1 = score1l
    plt.figure(figsize=(8,4))
    plt.plot(x,y1,"r-",linewidth=1,label=u'test error')
    plt.xlabel("size of training set")
    plt.ylabel("error rate")
    plt.title("size and error")
    plt.show()



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
