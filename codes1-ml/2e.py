import matplotlib.pyplot as plt



column1 = [0.01552935,0.02244884,0.07021708,0.00014045,0.0118557,0.00146626,0.00037409,-0.00317349,0.01288141,-0.00459894,0.05227472,0.11014825]
column2 = [0.0426,-0.0013,0.1551,0.0086, 0.0050,0.0024, -0.0012,-0.0249,0.0073,-0.0042,0.0576,0.0850]

plt.title("pairwise scatterplots")
plt.xlim(xmax=0.16,xmin=-0.03)
plt.ylim(ymax=0.16,ymin=-0.03)
plt.xlabel("x")
plt.ylabel("y")
plt.plot(column1,column2,'ro')
plt.show()
