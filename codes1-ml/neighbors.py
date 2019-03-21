import numpy as np
from read import DataUtils
from collections import defaultdict
import matplotlib.pyplot as plt
import os

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

def outImg(arrX, arrY,i):

    m, n = np.shape(arrX)
    path = "/Users/ruotianjiang/Downloads/pic1"
    img = np.array(arrX[i])
    img = img.reshape(28,28)
    outfile = str(i) + "_" +  str(arrY[i]) + ".png"
    plt.figure()
    plt.imshow(img, cmap = 'binary')
    plt.savefig(path + "/" + outfile)

def find_labels_train():
    train_X, train_y, test_X, test_y = main()
    all_dis = []

    for i in range(len(train_X)):
        dis = np.linalg.norm(train_X[i]-train_X[0])
        all_dis.append(dis)
    sorted_dis = np.argsort(all_dis)
    path = "/Users/ruotianjiang/Downloads/pic1"
    if not os.path.exists(path):
       os.mkdir(path)
    for i in range(0,2):
        outImg(train_X, train_y,sorted_dis[i])

def find_labels():
    train_X, train_y, test_X, test_y = main()
    all_dis = []

    for i in range(len(train_X)):
        dis = np.linalg.norm(train_X[i]-test_X[3])
        all_dis.append(dis)
    sorted_dis = np.argsort(all_dis)
    path = "/Users/ruotianjiang/Downloads/pic1"
    if not os.path.exists(path):
       os.mkdir(path)
    for i in range(0,5):
        outImg(train_X, train_y,sorted_dis[i])

if __name__ == "__main__":
    find_labels_train()
