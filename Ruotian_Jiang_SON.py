from __future__ import print_function
from pyspark import SparkConf, SparkContext
import sys
import itertools
import time
APP_NAME = "INF553"


def mapper(line):
    oldstring = line.split(",")
    movieId = int(oldstring[1])
    userID = int(oldstring[0])
    return (userID,movieId) if task == '1' else (movieId,userID)

def combination(frequent_item,size):
    out = []
    for i in range(len(frequent_item)):
        for j in range(i+1,len(frequent_item)):
            if (sorted(frequent_item[i])[:size-1] == sorted(frequent_item[j])[:size-1]) \
            and (tuple(sorted(set(frequent_item[i]).union(set(frequent_item[j])))[1:]) in frequent_item):
                out.append(tuple(sorted(set(frequent_item[i]).union(set(frequent_item[j])))))
    return out

def Priori_count(support):
    def my_map_partitions(partition):
        baskets = [i for i in partition]
        size = 0
        final_iterator = []
        itemsets = set([item for line in baskets for item in line])
        max_size = len(itemsets)
        while len(itemsets) != 0 and size < max_size:
            size += 1
            frequent_item = []
            for i in itemsets:
                count = 0
                for j in baskets:
                    if isinstance(i, int):
                        if i in j:
                            count += 1
                    else:
                        if set(i).issubset(j):
                            count += 1
                if count >= support:
                    if isinstance(i, int):
                        frequent_item.append(i)
                        final_iterator.append((i,1))
                    else:
                        frequent_item.append(tuple(i))
                        final_iterator.append((tuple(i),1))
            itemsets = set(tuple(sorted(i)) for i in itertools.combinations(tuple(frequent_item),2)) if size == 1 else combination(frequent_item,size)
        return iter(final_iterator)
    return my_map_partitions

def count_chunk(items):
    def my_map_partitions(partition):
        baskets = [i for i in partition]
        final_iterator = []
        for i in items:
            count = 0
            for j in baskets:
                if isinstance(i, int):
                    if i in j:
                        count += 1
                else:
                    if set(i).issubset(j):
                        count += 1
            final_iterator.append((i,count))
        return iter(final_iterator)
    return my_map_partitions

def main(sc,filename):
    start_time = time.time()
    data = sc.textFile(filename)
    header = data.first()
    data = data.filter(lambda line: line != header)
    data = data.map(mapper)
    data = data.groupByKey().map(lambda x : set(list(x[1])))
    p = data.getNumPartitions()
    support = float(threshold)/p
    items = data.mapPartitions(Priori_count(support)).groupByKey().map(lambda x :x[0]).collect()
    data = data.mapPartitions(count_chunk(items)).reduceByKey(lambda x, y: x + y)\
            .filter(lambda x: x[1] >= float(threshold)).map(lambda x :x[0]).sortBy(lambda x: x).collect()
    maxsize = max([len(x) if not isinstance(x, int) else 1 for x in data])
    f = open('Ruotian_Jiang_SON_%s.case%s-%s.txt' %(dataset_name,task,threshold), "w")
    f.write(', '.join('({})'.format(x) for x in [x for x in data if isinstance(x, int)]))
    line = 2
    while line <= maxsize:
        f.write('\n\n')
        f.write(', '.join('{}'.format(x) for x in [x for x in data if (not isinstance(x, int)) and len(x) == line]))
        line += 1
    f.close()
    print("--- %s seconds ---" % (time.time() - start_time))
    print (p)


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    task = sys.argv[1]
    filename = sys.argv[2]
    threshold = sys.argv[3]
    dataset_name = filename.split('/')[-1].split('.')[0]
    if dataset_name == 'ratings':
       filesize = filename.split('/')[-2]
       dataset_name = 'MovieLens.Big' if filesize == 'ml-20m' else 'MovieLens.Small'
    # Execute Main functionality
    main(sc, filename)
