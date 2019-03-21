from __future__ import print_function
from pyspark import SparkConf, SparkContext
import sys
import time
from collections import defaultdict
APP_NAME = "INF551"


def mapper_a(line):
    oldstring = [int(i) for i in line.replace('[', '').replace(']', '').replace('(', '').replace(')', '').strip('').split(",")]
    i = oldstring[0]
    k = oldstring[1]
    values = []
    res = []
    for t in range(2,len(oldstring),3):
        values.append(oldstring[t:t+3])
    value = ['A', k , values]
    for j in range(1,4):
        key = [i, j]
        res.append (key+value)
    return res

def mapper_b(line):
    oldstring = [int(i) for i in line.replace('[', '').replace(']', '').replace('(', '').replace(')', '').strip('').split(",")]
    j = oldstring[1]
    k = oldstring[0]
    values = []
    res = []
    for t in range(2,len(oldstring),3):
        values.append(oldstring[t:t+3])
    value = ['B', k , values]
    for i in range(1,4):
        key = [i, j]
        res.append(key + value)
    return res

def matrix_multiply(a,b):
    a1=a2=a3=a4=0
    for i in a:
        if i[:2] == [1,1]:
            a1 = i[2]
        if i[:2] == [1,2]:
            a2 = i[2]
        if i[:2] == [2,1]:
            a3 = i[2]
        if i[:2] == [2,2]:
            a4 = i[2]
    b1=b2=b3=b4=0
    for i in b:
        if i[:2] == [1,1]:
            b1 = i[2]
        if i[:2] == [1,2]:
            b2 = i[2]
        if i[:2] == [2,1]:
            b3 = i[2]
        if i[:2] == [2,2]:
            b4 = i[2]
    return [a1*b1+a2*b3,a1*b2+a2*b4,a3*b1+a4*b3,a3*b2+a4*b4]

def reducer(line):
    key = line[0]
    lists = sorted(line[1])
    list_a = [l for l in lists if l[0]=='A']
    list_b = [l for l in lists if l[0]=='B']
    origin = [[1,1,0],[1,2,0],[2,1,0],[2,2,0]]
    for i in range(len(list_a)):
        for j in range(len(list_b)):
            if list_a[i][1] == list_a[j][1]:
                res = matrix_multiply(list_a[i][2],list_b[j][2])
                for j in range(len(origin)):
                    origin[j][2] += res[j]
    origin = [i for i in origin if i[2] != 0]
    if origin:
        return [key,origin]




def main(sc,file_A,file_B,out_path):
    start_time = time.time()
    A = sc.textFile(file_A)
    B = sc.textFile(file_B)
    data_a = A.flatMap(mapper_a)
    data_b = B.flatMap(mapper_b)
    user_data = data_a.union(data_b).map(lambda x: (tuple(x[:2]),list(x[2:]))).groupByKey().map(lambda x : [x[0], list(x[1])]).map(reducer).collect()
    f = open(out_path+'/output.txt', "w")
    f.write('\n'.join('{}]]'.format(str(x).strip('[]')) for x in sorted([x for x in user_data if x is not None])))
    f.close()
    print("Time: %s sec" % (time.time() - start_time))


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    file_A = sys.argv[1]
    file_B = sys.argv[2]
    out_path = sys.argv[3]

    # Execute Main functionality
    main(sc,file_A,file_B,out_path)
