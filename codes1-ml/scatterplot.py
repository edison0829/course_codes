import csv
import matplotlib.pyplot as plt
import math



with open('/Users/ruotianjiang/Downloads/forestfires.csv','rb') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

column1 = [float(row[8]) for row in rows[1:]]
column2 = [math.log(1+float(row[12]),math.e) for row in rows[1:]]

plt.title("pairwise scatterplots")
plt.xlim(xmax=35,xmin=0)
plt.ylim(ymax=10,ymin=0)
plt.xlabel("x")
plt.ylabel("y")
plt.plot(column1,column2,'ro')
plt.show()
