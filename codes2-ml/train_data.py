import pandas as pd
import numpy as np



def train_data(n):

    path=[]

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




    # change value here
    x_train=[]
    y_train=[]
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
                x=[]
                setmean=list(data.loc[k*fragment:(k+1)*fragment-1].mean())
                setmax=list(data.loc[k*fragment:(k+1)*fragment-1].max())
                setmin=list(data.loc[k*fragment:(k+1)*fragment-1].min())
                x=setmean[1:]+setmax[1:]+setmin[1:]
                x_train.append(x)
                y_train.append(1)


    for i in range(2,7):
        for j in range(3,len(path[i])):
            if i == 1 and j ==3:
                data = pd.read_csv(path[i][j],header=4,delim_whitespace=True)

            else:
                data = pd.read_csv(path[i][j],header=4)

            fragment=len(data.index)//n
            for k in range(n):

                setmean=list(data.loc[k*fragment:(k+1)*fragment-1].mean())
                setmax=list(data.loc[k*fragment:(k+1)*fragment-1].max())
                setmin=list(data.loc[k*fragment:(k+1)*fragment-1].min())
                x=setmean[1:]+setmax[1:]+setmin[1:]

                x_train.append(x)
                y_train.append(0)
    return x_train , y_train


if __name__ == "__main__":
    a ,b =train_data()
    a=np.array(a)
    b=np.array(b)
    # print b
    # print np.transpose(b)
    print(a.shape)
    print(b.shape)
