import numpy as np
import struct
import matplotlib.pyplot as plt
import os
from read import DataUtils

trainfile_X = '/Users/ruotianjiang/Downloads/train-images-idx3-ubyte'
trainfile_y = '/Users/ruotianjiang/Downloads/train-labels-idx1-ubyte'
testfile_X = '/Users/ruotianjiang/Downloads/t10k-images-idx3-ubyte'
testfile_y = '/Users/ruotianjiang/Downloads/t10k-labels-idx1-ubyte'

train_X = DataUtils(filename=trainfile_X).getImage()
train_y = DataUtils(filename=trainfile_y).getLabel()
test_X = DataUtils(testfile_X).getImage()
test_y = DataUtils(testfile_y).getLabel()

path_trainset = "/Users/ruotianjiang/Downloads/imgs_train"
path_testset = "/Users/ruotianjiang/Downloads/imgs_test"
if not os.path.exists(path_trainset):
   os.mkdir(path_trainset)
if not os.path.exists(path_testset):
   os.mkdir(path_testset)
DataUtils(outpath=path_trainset).outImg(train_X, train_y)
DataUtils(outpath=path_testset).outImg(test_X, test_y)
