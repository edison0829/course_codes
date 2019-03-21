import csv

with open('/Users/ruotianjiang/Downloads/forestfires.csv','rb') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

row[0].append('area2')
for row in rows[1:]:
    row.append(math.log(1+float(row[-1]),math.e))

    with open('/Users/ruotianjiang/Downloads/forestfires.csv','w') as f2:
    writer = csv.writer(f2)
    
