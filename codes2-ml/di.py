# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from feature import get_data

mean, maxi, mini,median,var = get_data()
for a in [0,1,5]:
    mean_bending = [i[a] for k in mean[0:1] for i in k[2:]]
    mean_other = [i[a] for k in mean[2:] for i in k[3:]]

    maxi_bending = [i[a] for k in maxi[0:1] for i in k[2:]]
    maxi_other = [i[a] for k in maxi[2:] for i in k[3:]]

    mini_bending = [i[a] for k in mini[0:1] for i in k[2:]]
    mini_other = [i[a] for k in mini[2:] for i in k[3:]]


    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    #  将数据点分成三部分画，在颜色上有区分度
    ax.scatter(mean_other,maxi_other ,mini_other ,linewidths =0.5,marker='.', c='y')
    ax.scatter(mean_bending, maxi_bending, mini_bending,linewidths=0.5,marker='^', c='b')  # 绘制数据点


    ax.set_zlabel('mean')  # 坐标轴
    ax.set_ylabel('max')
    ax.set_xlabel('min')
    plt.show()
