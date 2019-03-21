from __future__ import print_function
from pyspark import SparkConf, SparkContext
from operator import add
import sys
import numpy as np
from collections import Counter
import itertools
import time
APP_NAME = "INF553"


def mapper(line):
    oldstring = line.split(",")
    UserId = int(oldstring[0][1:])
    movieID = [int(i) for i in oldstring[1:]]
    return (UserId,movieID)


def Signature(line):
    a_parameter =  [3]
    # random.shuffle(a_parameter)
    # h(x,i) = (3x + 13i) % 100
    b_parameter = range(0,20)
    movieId = line[1]
    userID = line[0]
    sig = []
    for a in a_parameter:
        for b in b_parameter:
            for p in [100]:
                candidates = []
                for i in movieId:
                    candidates.append((a*i + 13*b) % p)
                sig.append(min(candidates))
    return (userID,sig)

def Group(line):
    bands = 5
    rowsPerband = len(line[1])/bands
    split_list = []
    for i in range(bands):
        split_list.append((tuple(line[1][rowsPerband*i:rowsPerband*(i+1)])+(i,),line[0]))
    return split_list

def combine(data):
    split_list = []
    for i in data:
        if len(i) == 2:
            split_list.append(tuple(i))
        else:
            a = itertools.combinations(i, 2)
            split_list = split_list + list(a)
    return set(split_list)



def recommendations(refer):
    def _processDataLine(line):
        User = line[0]
        movies = []
        cands = sorted(line[1], key=lambda x: x[0], reverse=False)
        cands = sorted(cands, key=lambda x: x[1], reverse=True)
        for cand in cands[:5]:
            for movie in refer[cand[0]]:
                movies.append(movie)
        res = [[x,movies.count(x)] for x in set(movies)]
        res.sort(key=lambda x: x[0], reverse=False)
        res.sort(key=lambda x: x[1], reverse=True)
        return User, [i[0] for i in res[:3]]

    return _processDataLine

def main(sc,filename,outfile):
    start_time = time.time()
    data = sc.textFile(filename).map(mapper)
    refer_dict = data.map(lambda x :[x[0],set(x[1])]).collect()
    refer_dict = dict(refer_dict)
    data = data.map(Signature).flatMap(Group).groupByKey().map(lambda x : (x[0], list(x[1]))).\
    filter(lambda x: len(x[1]) >= 2).map(lambda x : sorted(x[1])).collect()
    out = []
    for i in combine(data):
        sim = float(len(refer_dict[i[0]].intersection(refer_dict[i[1]])))/float(len(refer_dict[i[0]].union(refer_dict[i[1]])))
        # jaccard function
        out.append((i,sim))
        out.append((i[::-1], sim))
    res = sc.parallelize(out).map(lambda x :[x[0][0],[x[0][1],x[1]]]).groupByKey().\
        map(lambda x : (x[0], list(x[1]))).map(recommendations(refer_dict)).sortBy(lambda a: a[0]).collect()
    print (res)
    f = open(outfile, "w")
    for x in res:
        f.write('U'+str(x[0])+',')
        f.write(str(x[1]).replace('[', '').replace(']', '').replace(' ',''))
        f.write('\n')
    f.close()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    filename = sys.argv[1]
    outfile = sys.argv[2]
    # Execute Main functionality
    main(sc, filename,outfile)
