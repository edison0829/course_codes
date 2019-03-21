import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def train_data():

    path=[]
    mean=[[],[],[],[],[],[],[]]
    maxi=[[],[],[],[],[],[],[]]
    mini=[[],[],[],[],[],[],[]]
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

    plt.title("features scatterplots")
    plt.xlim(xmax=10,xmin=0)
    # plt.ylim(ymax=0.16,ymin=-0.03)
    plt.xlabel("features")
    plt.ylabel("value")


    n=2
    # change value here

    for i in range(2,7):
        current=[]
        for j in range(15):
            current.append(root[i]+'dataset'+str(j+1)+'.csv')
        path.append(current)

    for i in range(0,2):
        for j in range(2,len(path[i])):
            if i == 1 and j ==3:
                data = pd.read_csv(path[i][j],header=4,names=['Columns: time','avg_rss12','var_rss12', 'avg_rss13', 'var_rss13', 'avg_rss23', 'var_rss23'],delim_whitespace=True)


            else:
                data = pd.read_csv(path[i][j],header=4)

            fragment=len(data.index)//n
            for k in range(n):
                subsetmean,subsetmax,subsetmin=[],[],[]
                setmean=list(data.loc[k*fragment:(k+1)*fragment-1].mean())

                plt.plot([1,2,3],[setmean[1],setmean[2],setmean[6]],'ro')
                setmax=list(data.loc[k*fragment:(k+1)*fragment-1].max())
                plt.plot([4,5,6],[setmax[1],setmax[2],setmax[6]],'ro')
                setmin=list(data.loc[k*fragment:(k+1)*fragment-1].min())
                plt.plot([7,8,9],[setmin[1],setmin[2],setmin[6]],'ro')
                subsetmean.append(setmean[1:])
                subsetmax.append(setmax[1:])
                subsetmin.append(setmin[1:])
            mean[i].append(subsetmean)
            maxi[i].append(subsetmax)
            mini[i].append(subsetmin)
    for i in range(2,7):
        for j in range(3,len(path[i])):
            if i == 1 and j ==3:
                data = pd.read_csv(path[i][j],header=4,delim_whitespace=True)

            else:
                data = pd.read_csv(path[i][j],header=4)

            fragment=len(data.index)//n
            for k in range(n):
                subsetmean,subsetmax,subsetmin=[],[],[]
                setmean=list(data.loc[k*fragment:(k+1)*fragment-1].mean())
                plt.plot([1,2,3],[setmean[1],setmean[2],setmean[6]],'y*',label='other')
                setmax=list(data.loc[k*fragment:(k+1)*fragment-1].max())
                plt.plot([4,5,6],[setmax[1],setmax[2],setmax[6]],'y*')
                setmin=list(data.loc[k*fragment:(k+1)*fragment-1].min())
                plt.plot([7,8,9],[setmin[1],setmin[2],setmin[6]],'y*')
                subsetmean.append(setmean[1:])
                subsetmax.append(setmax[1:])
                subsetmin.append(setmin[1:])
            mean[i].append(subsetmean)
            maxi[i].append(subsetmax)
            mini[i].append(subsetmin)
    names=['mean_S1','mean_S2','mean_S3','max_S1','max_S2','max_S3','min_S1','min_S2','min_S3']
    plt.xticks(range(1,10),names,rotation = 45)
    plt.show()
    return mean, maxi, mini


# def output():
#     # mean, maxi, mini,median,var = get_data()
#     #
#     # print "mean: "
#     # print mean
#     # print "max: "
#     # print maxi
#     # print "min: "
#     # print mini
#     # print "median: "
#     # print median
#     # print "variance: "
#     # print var
if __name__ == "__main__":
    train_data()
