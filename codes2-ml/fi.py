import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import label_binarize
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt

def train_data():

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

            x=[]
            setmean=list(data.mean())
            setmax=list(data.max())
            setmin=list(data.min())
            x=setmean[1:]+setmax[1:]+setmin[1:]
            x_train.append(x)
            y_train.append(i)


    for i in range(2,7):
        for j in range(3,len(path[i])):
            if i == 1 and j ==3:
                data = pd.read_csv(path[i][j],header=4,delim_whitespace=True)

            else:
                data = pd.read_csv(path[i][j],header=4)

            setmean=list(data.mean())
            setmax=list(data.max())
            setmin=list(data.min())
            x=setmean[1:]+setmax[1:]+setmin[1:]

            x_train.append(x)
            y_train.append(i)
    return x_train , y_train


if __name__ == "__main__":
    X_train,y_train =train_data()
    X_train=np.array(X_train)
    y_train=np.array(y_train)
    clf = LogisticRegression(penalty='l1',multi_class='ovr',solver='liblinear')
    clf.fit(X_train, y_train)
    print(clf.score(X_train,y_train))


    y_pred=clf.predict(X_train)
    cnf_matrix = confusion_matrix(y_train, y_pred)
    print(cnf_matrix)

    y_train= label_binarize(y_train, classes=[0,1,2,3,4,5,6])
    n_classes = 7
    # classifier
    # clf = OneVsRestClassifier(LinearSVC(random_state=0))
    y_score = clf.decision_function(X_train)




    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_train[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Plot of a ROC curve for a specific class
    for i in range(n_classes):
        plt.figure()
        plt.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f)' % roc_auc[i])
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
