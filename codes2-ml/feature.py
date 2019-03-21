import pandas as pd
import numpy as np



def get_data():

    path=[]
    mean=[[],[],[],[],[],[],[]]
    maxi=[[],[],[],[],[],[],[]]
    mini=[[],[],[],[],[],[],[]]
    median=[[],[],[],[],[],[],[]]
    var=[[],[],[],[],[],[],[]]
    root1='/Users/ruotianjiang/Downloads/AReM/bending1/'
    root2='/Users/ruotianjiang/Downloads/AReM/bending2/'
    root3='/Users/ruotianjiang/Downloads/AReM/cycling/'
    root4='/Users/ruotianjiang/Downloads/AReM/lying/'
    root5='/Users/ruotianjiang/Downloads/AReM/sitting/'
    root6='/Users/ruotianjiang/Downloads/AReM/standing/'
    root7='/Users/ruotianjiang/Downloads/AReM/walking/'
    root=[root1,root2,root3,root4,root5,root6,root7]
    path.append([root1+'dataset1.csv',root1+'dataset2.csv',root1+'dataset3.csv',root1+'dataset4.csv',root1+'dataset5.csv',root1+'dataset6.csv',root1+'dataset7.csv'])
    path.append([root2+'dataset1.csv',root2+'dataset2.csv',root2+'dataset3.csv',root2+'dataset4.csv',root2+'dataset5.csv',root2+'dataset6.csv'])
    for i in range(2,7):
        current=[]
        for j in range(15):
            current.append(root[i]+'dataset'+str(j+1)+'.csv')
        path.append(current)

    for i in range(7):
        for j in range(len(path[i])):
            if i == 1 and j ==3:
                data = pd.read_csv(path[i][j],header=4,names=['Columns: time','avg_rss12','var_rss12', 'avg_rss13', 'var_rss13', 'avg_rss23', 'var_rss23'],delim_whitespace=True)

            else:
                data = pd.read_csv(path[i][j],header=4)
            setmean=list(data.mean())
            setmax=list(data.max())
            setmin=list(data.min())
            setmedian=list(data.median())
            setvar=list(data.var())
            mean[i].append(setmean[1:])
            maxi[i].append(setmax[1:])
            mini[i].append(setmean[1:])
            median[i].append(setmedian[1:])
            var[i].append(setvar[1:])
    return mean, maxi, mini,median,var


def output():
    mean, maxi, mini,median,var = get_data()

    print "mean: "
    print mean
    print "max: "
    print maxi
    print "min: "
    print mini
    print "median: "
    print median
    print "variance: "
    print var


if __name__ == "__main__":
    output()
