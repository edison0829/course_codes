from __future__ import print_function
from pyspark import SparkConf, SparkContext
import sys
from collections import defaultdict
APP_NAME = "INF553"


def mapper(line):
    oldstring = line.replace("[","").replace("]","").replace("\"","").split(",")
    a = oldstring[0]
    b = oldstring[1]
    return a,b


def bfs_connected_component(graph):
    def _processDataLine(start):
        queue = [start]
        levels = {}         # this dict keeps track of levels
        levels[start]= 0    # depth of start node is 0
        visited= set([start])     # to avoid inserting the same node twice into the queue
        # keep looping until there are nodes still to be checked
        while queue:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            neighbours = graph[node]
            # add neighbours of node to queue
            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)
                    levels[neighbour]= levels[node]+1
                    # print(neighbour, ">>", levels[neighbour])
        CreditsForPoint = {}
        CreditsForEdge = set([])
        noteValue = {}
        noteValue[start]=1
        v = defaultdict(list)
        value_list = []
        for key, value in sorted(levels.iteritems()):
            value_list.append(value)
            v[value].append(key)
        depth = max(value_list)
        for i in range(1, depth + 1):
            for j in v[i]:
                note = 0
                for k in graph[j]:
                    if levels[k] < i:
                        note += noteValue[k]
                noteValue[j] = note
        for i in range(0, depth + 1)[::-1]:
            row = v[i]
            if i == depth:
                for j in row:
                    CreditsForPoint[j] = 1
            else:
                for j in row:
                    children = []
                    for link in graph[j]:
                        if levels[link] > i:
                            children.append(link)
                    if len(children) == 0:
                        CreditsForPoint[j] = 1
                    else:
                        CreditsForPoint[j] = 1
                        for child in children:
                            out = sorted((child, j))
                            C = CreditsForPoint[child]*(noteValue[j]/float(noteValue[child]))
                            CreditsForEdge.add(((out[0],out[1]),C))
                            CreditsForPoint[j] += C
        return CreditsForEdge
    return _processDataLine


def main(sc,file,output):
    edge_data = sc.textFile(file)
    edge_data = edge_data.map(mapper)
    graph_data = edge_data.map(lambda x:[x[0],x[1]]).groupByKey().map(lambda x : [x[0], list(x[1])])
    graph_data_reverse = edge_data.map(lambda x:[x[1],x[0]]).groupByKey().map(lambda x: [x[0], list(x[1])])
    graph = sc.union([graph_data, graph_data_reverse]).reduceByKey(lambda a, b: a + b).collect()
    graph_dict = dict(graph)
    output_data = sc.parallelize(list(graph_dict.keys())).flatMap(bfs_connected_component(graph_dict)) \
            .reduceByKey(lambda a, b: a + b).map(lambda x : (x[0], x[1]/2.0)).collect()
    f = open(output, "w")
    for i in sorted(output_data):
        i = [tuple([k.encode("utf-8") for k in i[0]]),i[1]]
        f.write(str(i).replace("[","").replace("]","").replace("\'",""))
        f.write('\n')
    f.close()


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    file = sys.argv[1]
    output = sys.argv[2]

    # Execute Main functionality
    main(sc,file,output)
