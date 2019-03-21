import sys
import pycrfsuite
import nltk
import re



crf_model = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

def feature_generate(words):
    features = []
    # Perform POS tagging
    tagged = [j for i,j in nltk.pos_tag(words)]
    for i in range(len(words)):
        word = words[i]
        postag  = tagged[i]
        # Common features for all words
        f = [
            'bias',
            'word.lower=' + word.lower(),
            'word[-3:]=' + word[-3:],
            'word[-2:]=' + word[-2:],
            'word.isupper=%s' % word.isupper(),
            'word.istitle=%s' % word.istitle(),
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag
        ]

        # Features for words that are not
        # at the beginning of a document
        if i > 0:
            word1 = words[i - 1]
            postag1 = tagged[i - 1]
            f.extend([
                '-1:word.lower=' + word1.lower(),
                '-1:word.istitle=%s' % word1.istitle(),
                '-1:word.isupper=%s' % word1.isupper(),
                '-1:word.isdigit=%s' % word1.isdigit(),
                '-1:postag=' + postag1
            ])
        else:
            # Indicate that it is the 'beginning of a document'
            f.append('BOS')

        # Features for words that are not
        # at the end of a document
        if i < len(doc) - 1:
            word1 = words[i + 1]
            postag1 = tagged[i + 1]
            f.extend([
                '+1:word.lower=' + word1.lower(),
                '+1:word.istitle=%s' % word1.istitle(),
                '+1:word.isupper=%s' % word1.isupper(),
                '+1:word.isdigit=%s' % word1.isdigit(),
                '+1:postag=' + postag1
            ])
        else:
            # Indicate that it is the 'end of a document'
            f.append('EOS')
        features.append(f)
    return features


def concatenate(L):
    cur = L[0]
    res = [[L[0],0]]
    for i in range(1,len(L)):
        if L[i] != cur:
            cur = L[i]
            res[-1][-1] = i-1
            res.append([cur,0])
    res[-1][-1] = len(L) - 1
    return res



tagger = pycrfsuite.Tagger()
tagger.open(crf_model)
text_file = open(input_file, "r")
lines = text_file.readlines()
test_y = []
test_x = []
for line in lines:
    chunks = line.split('> ')
    testset = []
    doc = []
    label = []
    for chunk in chunks:
        name = chunk.split('>')[0][1:]
        words = chunk.split('>')[1].split('<')[0].split(' ')
        # for sentence in sentences:
        #     print (sentence)
        #     features = feature_generate()
        for i in range(len(words)):
            word = words[i].strip(',.;')
            doc.append(word)
            label.append(name)
    features = feature_generate(doc)
    test_y.append(label)
    test_x.append(features)



y_pred = [tagger.tag(a) for a in test_x]


# generate the output with tag
with open(output_file, 'w') as the_file:
    for i in range(len(y_pred)):
        fill_dict = concatenate(y_pred[i])
        out = re.sub(r'\<.*?\>', '', lines[i]).strip('\n').split(' ')
        out[0] = '<'+ fill_dict[0][0] + '>' + out[0]
        for f in range(len(fill_dict)-1):
            out[fill_dict[f][1]] = out[fill_dict[f][1]] + '</' + fill_dict[f][0] + '>'
            out[fill_dict[f][1]+1] = '<' + fill_dict[f+1][0] + '>' + out[fill_dict[f][1]+1]
        out[-1] = out[-1] + '</' + fill_dict[-1][0] + '>'
        the_file.write(' '.join(out) + '\n')

the_file.close()


# estimate
TP = 0
FN = 0
FP = 0
for i in range(len(y_pred)):
    pred = concatenate(y_pred[i])
    truth = concatenate(test_y[i])
    FP += len([item for item in pred if item not in truth])
    FN += len([item for item in truth if item not in pred])
    TP += len([item for item in pred if item in truth])
    # if pred != truth:
    #     index_p = [a[1] for a in pred]
    #     index_t =  [a[1] for a in truth]
    #     if index_t == index_p:
    #         FP += len([item for item in pred if item not in truth])
    #         TP += len([item for item in pred if item in truth])
    #     else:
    #         if len(index_p) != len(index_t):
    #             FN += len([item for item in index_p if item not in index_t])
    #             FP += len([item for item in index_t if item not in index_p])
    #             TP += len([item for item in index_t if item in index_p])
    #         else:
    #             pre = -2
    #             for j in range(len(index_p)):
    #                 if index_p[j] != index_t[j]:
    #                     # the diff is connected
    #                     if j - pre == 1:
    #                         FN += 1
    #                         FP += 1
    #                     # the diff is not connected
    #                     else:
    #                         FN += 2
    #                         FP += 2
    #                     pre = j
    # else:
    #     TP += len(pred)
precision = TP/float(TP+FP)
recall = TP/float(TP+FN)
f1 = 2*precision*recall/(precision+recall)
print ('precision: %s' % precision)
print ('recall: %s' % recall)
print ('F1 score: %s' % f1)




