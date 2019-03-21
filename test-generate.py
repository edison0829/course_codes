import json



with open('results/Chemical Engineering.json') as f:
    data = json.load(f)
with open('test-ucla.txt', 'a') as the_file:
    for i in data['courses'][33:83]:
        print (i['Course description'])
        the_file.write(i['Course description'])
        the_file.write('\n')
