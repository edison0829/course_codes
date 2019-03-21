from feature import get_data
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats

def bootstrap(data, num_samples, statistics, alpha):
    n = len(data)
    idx = np.random.randint(0, n, size=(num_samples, n))
    samples = data[idx]
    stat = np.sort(statistics(samples, 1))
    return (stat[int((alpha/2)*num_samples)], stat[int((1-alpha/2)*num_samples)])

mean, maxi, mini,median,var = get_data()
def std_deviation(set):
    Xstd1=[]
    Xstd2=[]
    Xstd3=[]
    Xstd4=[]
    Xstd5=[]
    Xstd6=[]
    for k in set:
        goal1=[]
        goal2=[]
        goal3=[]
        goal4=[]
        goal5=[]
        goal6=[]
        for i in k:
            goal1.append(i[0])
            goal2.append(i[1])
            goal3.append(i[2])
            goal4.append(i[3])
            goal5.append(i[4])
            goal6.append(i[5])
        Xstd1.append(np.std(goal1))
        Xstd2.append(np.std(goal2))
        Xstd3.append(np.std(goal3))
        Xstd4.append(np.std(goal4))
        Xstd5.append(np.std(goal5))
        Xstd6.append(np.std(goal6))
    return [Xstd1,Xstd2,Xstd3,Xstd4,Xstd5,Xstd6]


print "mean_std: "
print std_deviation(mean)
print "bootsrap confidence interval: "
output=std_deviation(mean)
for i in output:
    print  bootstrap(np.array(i), 100000, np.mean, 0.05)
print "max_std: "
print std_deviation(maxi)
print "bootsrap confidence interval: "
output=std_deviation(maxi)
for i in output:
    print  bootstrap(np.array(i), 100000, np.mean, 0.05)
print "min: "
print std_deviation(mini)
print "bootsrap confidence interval: "
output=std_deviation(mini)
for i in output:
    print  bootstrap(np.array(i), 100000, np.mean, 0.05)
print "median: "
print std_deviation(median)
print "bootsrap confidence interval: "
output=std_deviation(median)
for i in output:
    print  bootstrap(np.array(i), 100000, np.mean, 0.05)
print "variance: "
print std_deviation(var)
print "bootsrap confidence interval: "
output=std_deviation(var)
for i in output:
    print  bootstrap(np.array(i), 100000, np.mean, 0.05)
