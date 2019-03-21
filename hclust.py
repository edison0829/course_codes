import sys
import heapq
import numpy as np
from scipy.spatial import distance
import itertools

# def Euclidean(x,y):
#     return  np.linalg.norm(np.array(x)-np.array(y))

# def dist(x, y):
#     vec_x = np.array(x)
#     vec_y = np.array(y)
#     result = np.sqrt(np.sum(np.square(vec_x - vec_y)))
#     return result
def center(x,y,pos):
    len_x = len([int(j) for j in str(x).replace('(','').replace(')','').split(',')])
    len_y = len([int(j) for j in str(y).replace('(','').replace(')','').split(',')])
    x = np.array(pos[x])
    y = np.array(pos[y])
    output = (x*len_x+y*len_y)/(len_x+len_y)
    output = output.tolist()
    return output


def clustering(heap,pos,k,valid,original_k):
    while heap:
        cur_node = heapq.heappop(heap)
        cur_node = cur_node[1]
        if cur_node[0] in valid and cur_node[1] in valid:
            original_k -= 1
            new_data = center(cur_node[0],cur_node[1],pos)
            pos[cur_node] = new_data
            valid.remove(cur_node[0])
            valid.remove(cur_node[1])
            for i in valid:
                dis = distance.euclidean(pos[i], new_data)
                # dis = dist(pos[i],new_data)
                heapq.heappush(heap, [dis, (cur_node, i)])
            valid.add(cur_node)
            if original_k == k:
                # print cur_node
                # print pos[73]
                # print pos[(63,78,91)]
                # print distance.euclidean(pos[cur_node[0]], pos[cur_node[1]])
                return list(valid)


def main(file,k):
    # read the file
    with open(file) as f:
        data = []
        for line in f:
            row = line.strip('\n').split(',')
            data.append([float(i) for i in row[:4]]+row[4:])
    f.close()
    # processing the data
    original_k = len(data)
    valid = set(range(len(data)))
    heap = []
    truth_pairs = []
    pos = {}
    for i in range(len(data)):
        pos[i] = data[i][:4]
        for j in range(i+1,len(data)):
            if data[i][4] == data[j][4]:
                truth_pairs.append((i,j))
            dis = distance.euclidean(data[i][:4],data[j][:4])
            heapq.heappush(heap,[dis,(i,j)])
    result = clustering(heap, pos, int(k), valid, original_k)
    total_precision = 0
    total_recall = len(truth_pairs)
    score = 0
    # output and evaluation
    for i in range(len(result)):
        cur_class = sorted([int(j) for j in str(result[i]).replace('(','').replace(')','').split(',')])
        print ("Cluster%s: %s" % (i+1, cur_class))
        for k in range(len(cur_class)):
            for s in range(k+1,len(cur_class)):
                if (cur_class[k],cur_class[s]) in truth_pairs:
                    score += 1
                total_precision += 1
    print ("Precision = %s, recall = %s" % (float(score)/total_precision, float(score)/total_recall))


if __name__ == "__main__":
    filename = sys.argv[1]
    k = sys.argv[2]
    # Execute Main functionality
    main(filename,k)