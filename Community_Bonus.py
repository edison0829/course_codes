
from networkx.algorithms import community
from pyspark import SparkConf, SparkContext
import sys
import networkx as nx
import time
APP_NAME = "INF553"


def mapper(line):
    oldstring = line.split(",")
    movieId = int(oldstring[1])
    userID = int(oldstring[0])
    return userID,movieId


def cal(user_list):
    output = []
    for i in range(len(user_list)):
        for j in range(i+1,len(user_list)):
            if len(set(user_list[i][1]).intersection(set(user_list[j][1]))) >= 9:
                output.append(sorted([user_list[i][0],user_list[j][0]]))
    return output


def main(sc,file):
    start_time = time.time()
    userfile = sc.textFile(file)
    header = userfile.first()
    user_data = userfile.filter(lambda line: line != header).map(mapper).groupByKey().map(lambda x : [x[0], list(x[1])])
    user_list = (user_data.collect())
    edges = cal(user_list)
    G = nx.Graph()
    G.add_edges_from(edges)
    communities_generator = community.asyn_fluidc(G, 100)
    output = [sorted(i) for i in communities_generator]
    f = open('Ruotian_Jiang_Community_Bonus.txt', "w")
    f.write('\n'.join('[{}]'.format(str(x).replace('[', '').replace(']', '')) for x in sorted(output)))
    f.close()
    print("Time: %s sec" % (time.time() - start_time))


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    file = sys.argv[1]

    # Execute Main functionality
    main(sc,file)