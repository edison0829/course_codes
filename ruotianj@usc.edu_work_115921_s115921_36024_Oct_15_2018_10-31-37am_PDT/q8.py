import distsim
from prettytable import PrettyTable
# Adversarial1(comparative):
#
# good bad better worse
# old young hot cold
# worst best happy sad
#
# Adversarial2(gender):
#
# brother sister son daughter
# dad mom king queen
# grandfather grandmother prince princess
lines1 = ['good bad better worse',
          'old young hot cold',
          'worst best happy sad']

lines2 = ['brother sister son daughter',
          'dad mom king queen',
          'grandfather grandmother prince princess']

def table(lines):
    data = []
    for line in lines:
        data.append(line.split(' '))
    data = [data]
    t = PrettyTable(['Class', '1-best','5-best','10-best'])
    title = ['adversarial1','adversarial2']
    p = [1,5,10]
    for num in range(len(data)):
        total = len(data[num])
        count = [0,0,0]
        for row in data[num]:
            word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
            w1 = word_to_vec_dict[row[0]]
            w2 = word_to_vec_dict[row[1]]
            w4 = word_to_vec_dict[row[3]]
            ret = distsim.show_nearest(word_to_vec_dict,
                                       w1 - w2 + w4,
                                       set([row[0], row[1], row[3]]),
                                       distsim.cossim_dense)
            true = row[2]
            for i in range(len(p)):
                l =  [j[0] for j in ret[:p[i]]]
                if true in l:
                    count[i] += 1
        t.add_row([title[num],count[0] / float(total),count[1] / float(total),count[2] / float(total)])
    print t

table(lines1)
table(lines2)