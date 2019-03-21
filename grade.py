import sys
import pyspark
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext
from operator import add
import itertools

sc = SparkContext.getOrCreate()
sqlContext=SQLContext(sc)
inputfile=sys.argv[1]
outputfile=sys.argv[2]
G = sc.textFile(inputfile).map(lambda x:eval(x))
G.collect()

def getNode(graph):
    node=[]
    for edge in graph:
        node+=edge
    return list(set(node))

def BFS(startnode,G):
    DAG=[]
    nodes=getNode(G)
    traveled_nodes=[]
    curlevel=[startnode]
    LevelNode=[[startnode]]
    graph=[x for x in G]
    while(len(traveled_nodes)<len(nodes) and len(graph)>0):
        traveled_nodes+=curlevel
        nextlevel=[]
        for node in curlevel:
            for edge in graph:
                if node in edge:
                    nextnode=edge[0] if edge[0]!=node else edge[1]
                    if nextnode in traveled_nodes or nextnode in nextlevel:
                        continue
                    nextlevel.append(nextnode)
        curlevel=nextlevel
        LevelNode.append(nextlevel)
        for node in traveled_nodes:
            for edge in graph:
                if node in edge:
                    graph.remove(edge)
                    continue
    LevelNode=LevelNode[0:-1]
    for i in range(len(LevelNode)-1):
        for e in list(itertools.product(LevelNode[i],LevelNode[i+1])):
            if list(e) in G or list(e)[::-1] in G:
                DAG.append(list(e))
    return DAG,LevelNode
#BFS(u'g',[x for x in input_graph])

def ComputeToNodeP(DAG):
    P={}
    P[DAG[0][0]]=1
    for edge in DAG:
        P.setdefault(edge[1],0)
        P[edge[1]]+=P[edge[0]]
    return P
#P=ComputeToNodeP(BFS(u'g',[x for x in input_graph])[0])
#P

def GetNodeParentesP(DAG,P):
    P_parents={}
    for edge in DAG:
        P_parents.setdefault(edge[1],0)
        P_parents[edge[1]]+=P[edge[0]]
    return P_parents

def ComputeFractionF(DAG,P,LevelNode):
    f={}
    P_parents=GetNodeParentesP(DAG,P)
    for leafnode in LevelNode[-1]:
        f[leafnode]=1
    for edge in DAG[::-1]:
        f.setdefault(edge[0],P[edge[0]])
        if edge[1] not in f.keys():
            f[edge[1]]=1
        f[edge[0]]+=f[edge[1]]*(float(P[edge[0]])/P_parents[edge[1]])
    fE={}
    P_parents=GetNodeParentesP(DAG,P)
    for edge in DAG:
        fE[tuple(set(edge))]=(float(P[edge[0]])/P_parents[edge[1]])*f[edge[1]]
    return fE

Nodes=list(set(G.reduce(add)))
StartNodes=G.flatMap(lambda x:[(k,x)for k in Nodes]).groupByKey().mapValues(lambda x:list(x))
StartNodes.collect()

DAGRDD=StartNodes.map(lambda (k,v):(k,BFS(k,v)))
DAGRDD.collect()


#ComputeToNodeP
#ComputeFractionF
fractionRDD=DAGRDD.map(lambda (k,v):(v,ComputeToNodeP(v[0])))

fractionRDD=fractionRDD.map(lambda x:ComputeFractionF(x[0][0],x[1],x[0][1])).flatMap(lambda d:[(x,d[x]) for x in d.keys()])
betRDD=fractionRDD.reduceByKey(add).mapValues(lambda x:x/2.0)
res=sorted(betRDD.collect())

betw=[]
print G.collect()
for edge in G.collect():
    for i in range(len(res)):
        if edge==list(res[i][0]) or edge[::-1]==list(res[i][0]):
            betw.append((edge,res[i][1]))
print betw

f=open(outputfile,'w')
for pair in betw:
    f.write('('+pair[0][0]+','+pair[0][1]+'),')
    f.write(str(pair[1]))
    f.write('\r\n')
f.close()

