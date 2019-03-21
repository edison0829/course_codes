import distsim
from prettytable import PrettyTable

lines = [line.rstrip('\n') for line in open('word-test.v3.txt')]
data = []
cur = []
for line in lines[1:]:
    if ':' in line:
        data.append(cur)
        cur = []
    else:
        cur.append(line.split(' '))
data.append(cur)
data = data[1:]
t = PrettyTable(['Class', '1-best','5-best','10-best'])
#     capi- tal 0, currency 1, city-in-state 2, family 3, adjective-to-adverb 4, comparative 5, superlative 6, and nationality-adjective 7.
title = ['capital', 'currency', 'city-in-state', 'family', 'adjective-to-adverb', 'comparative', 'superlative', 'nationality-adjective']
p = [1,5,10]
for num in range(len(data)):
    total = len(data[num])
    count = [0,0,0]
    e = []
    for row in data[num]:
        word_to_vec_dict = distsim.load_word2vec("deps.words")
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
            elif p[i] == 1:
                e.append([ret[0][0],true])
    t.add_row([title[num],count[0] / float(total),count[1] / float(total),count[2] / float(total)])
print t
# show an example of an incorrectly predicted analogy item, along with the correct answer.
# Are there certain kinds of relations that seem to be predicted more accurately or less accurately by this method?
# Discuss your opinions and give a rationale for them.