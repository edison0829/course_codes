from __future__ import print_function
from pyspark import SparkConf, SparkContext
import sys
import time
from collections import defaultdict
APP_NAME = "ISI_Challenge"


def mapper(line):
    oldstring = line.split(",")
    Q_Id = int(oldstring[0])
    userID = int(oldstring[1])
    return userID,Q_Id


def cal(user_list):
    output = []
    for i in range(len(user_list)):
        for j in range(i+1,len(user_list)):
            if len(set(user_list[i][1]).intersection(set(user_list[j][1]))) >= 1:
                # we can change the Threshold value here
                output.append(tuple(sorted([user_list[i][0],user_list[j][0]])))
    return output


def bfs(graph,start):
    queue = [start]
    levels = {}  # this dict keeps track of levels
    levels[start] = 0  # depth of start node is 0
    visited = set([start])  # to avoid inserting the same node twice into the queue
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        d = queue.pop(0)
        neighbours = graph[d]
        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)
                levels[neighbour] = levels[d] + 1
                # print(neighbour, ">>", levels[neighbour])
    return levels,visited

def test_bfs(graph,start):
    queue = set([start])
    visited = set([start])  # to avoid inserting the same node twice into the queue
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        d = queue.pop()
        neighbours = graph[d]
        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour not in visited:
                queue.add(neighbour)
                visited.add(neighbour)
    return visited

def test(graph,start):
    queue = set([start[0]])
    visited = set([start[0]])
    while queue:
        # pop shallowest node (first node) from queue
        d = queue.pop()
        neighbours = graph[d]
        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour == start[1]:
                return False
            if neighbour not in visited:
                queue.add(neighbour)
                visited.add(neighbour)
    return True


def betweenness(graph):
    def _processDataLine(start):
        levels, visited = bfs(graph,start)
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


def Q_sum(graph_dict,user_list,users,M):
    m = M
    Q = 0
    N = users
    for i in N:
        for j in N:
            A = 1 if tuple(sorted([i,j])) in user_list else 0
            Q = Q + A - graph_dict[i]*graph_dict[j]/float(2*m)
    return Q/(2*m)


def main(sc,file):
    start_time = time.time()
    userfile = sc.textFile(file)
    header = userfile.first()
    user_data = userfile.filter(lambda line: line != header).map(mapper).groupByKey().map(lambda x : [x[0], list(x[1])]).collect()
    user_list = cal(user_data)
    edge_data = sc.parallelize(user_list)
    graph_data = edge_data.map(lambda x:[x[0],x[1]]).groupByKey().map(lambda x : [x[0], list(x[1])])
    graph_data_reverse = edge_data.map(lambda x:[x[1],x[0]]).groupByKey().map(lambda x: [x[0], list(x[1])])
    graph = sc.union([graph_data, graph_data_reverse]).reduceByKey(lambda a, b: a + b).collect()
    graph_dict = dict(graph)
    original_dict = dict(graph_dict)
    m = len(user_list)
    for k, v in original_dict.iteritems():
        original_dict[k] = len(v)
    cur_modularity = Q_sum(original_dict,set([tuple(sorted(i)) for i in user_list]),tuple(graph_dict.keys()),m)
    print (cur_modularity)
    max_modularity = -1
    num = 1
    split_list = set([tuple(sorted(test_bfs(graph_dict, i))) for i in graph_dict.keys()])
    print (split_list)
    max_list = set([])
    edges_sort = sc.parallelize(list(graph_dict.keys())).flatMap(betweenness(graph_dict)) \
        .reduceByKey(lambda a, b: a + b).map(lambda x: (x[0], x[1] / 2.0)).sortBy(lambda x: -x[1])
    print (edges_sort.collect())
    edges_sort = edges_sort.map(lambda x: x[0]).collect()
    edges = set([tuple(sorted(i)) for i in edges_sort])
    while edges_sort:
        while len(split_list) <= num:
            cur_edge = edges_sort.pop(0)
            graph_dict[cur_edge[0]].remove(cur_edge[1])
            graph_dict[cur_edge[1]].remove(cur_edge[0])
            if test(graph_dict, cur_edge):
                cur_cut = set([tuple(sorted(test_bfs(graph_dict, i))) for i in cur_edge])
                cur_list = set([x for x in split_list if cur_edge[1] not in set(x)])
                split_list = cur_list.union(cur_cut)
        cur_modularity = 0
        for each in split_list:
            cur_modularity += Q_sum(original_dict,edges,each,m)
        if cur_modularity >= max_modularity:
            max_modularity = cur_modularity
            max_list = split_list
        print(num)
        print(cur_modularity)
        num += 1
    output = max_list
    f = open('result.txt', "w")
    f.write('\n'.join('[{}]'.format(str(list(x)).replace('[', '').replace(']', '')) for x in sorted(output)))
    f.close()
    print("Time: %s sec" % (time.time() - start_time))


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    file = sys.argv[1]

    # Execute Main functionality
    main(sc,file)
