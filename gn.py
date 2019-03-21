from __future__ import print_function
import sys
from collections import defaultdict
import json


def read(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def dict_bulid(data):
    data = data + [i[::-1] for i in data]
    out_dict = {}
    for p in data:
        if p[0] in out_dict:
            out_dict[p[0]].append(p[1])
        else:
            out_dict[p[0]] = [p[1]]
    return out_dict



def bfs_connected_component(graph,start):
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


def main(file,output):
    output_data = []
    edge_data = read(file)
    graph_dict = dict_bulid(edge_data)
    credit_dict = {}
    for key in graph_dict:
        cur_res = bfs_connected_component(graph_dict,key)
        for c in cur_res:
            if c[0] in credit_dict:
                credit_dict[c[0]] += c[1]
            else:
                credit_dict[c[0]] = c[1]
    for key, value in credit_dict.iteritems():
        temp = [key, value/2]
        output_data.append(temp)
    f = open(output, "w")
    for i in sorted(output_data):
        i = [tuple([k.encode("utf-8") for k in i[0]]),i[1]]
        f.write(str(i).replace("[","").replace("]","").replace("\'",""))
        f.write('\n')
    f.close()


if __name__ == "__main__":
    file = sys.argv[1]
    output = sys.argv[2]
    # Execute Main functionality
    main(file,output)


# output should like this:
# (a, b), 5.0
# (a, e), 2.0
# (b, c), 9.0
# (b, e), 3.0
# (b, f), 4.0
# (c, d), 8.0
# (d, g), 6.0
# (d, h), 7.0
# (e, f), 4.0
# (f, g), 7.0
# ["a","b"]
# ["a","e"]
# ["b","c"]
# ["b","e"]
# ["b","f"]
# ["c","d"]
# ["d","g"]
# ["d","h"]
# ["e","f"]
# ["f","g"]