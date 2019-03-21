
import random
f = open('out.txt', "w")
for x in range(1,101):
    f.write('U' + str(x) + ',')
    lenth = random.randint(1, 20)
    l = random.sample(range(0, 100), lenth)
    f.write(str(sorted(l)).replace('[', '').replace(']', '').replace(' ', ''))
    f.write('\n')
f.close()
# print("--- %s seconds ---" % (time.time() - start_time))