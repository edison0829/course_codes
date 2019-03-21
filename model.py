import pycrfsuite
import nltk

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


trainer = pycrfsuite.Trainer(verbose=True)
text_file = open("train-ucla.txt", "r")
lines = text_file.readlines()
train_y = []
train_x = []
for line in lines:
    thunks = line.split('> ')
    testset = []
    doc = []
    label = []
    for thunk in thunks:
        name = thunk.split('>')[0][1:]
        words = thunk.split('>')[1].split('<')[0].split(' ')
        # for sentence in sentences:
        #     print (sentence)
        #     features = feature_generate()
        for i in range(len(words)):
            word = words[i].strip(',.;')
            doc.append(word)
            label.append(name)
    features = feature_generate(doc)
    train_y.append(label)
    train_x.append(features)

for xseq, yseq in zip(train_x, train_y):
    trainer.append(xseq, yseq)
# Set the parameters of the model
trainer.set_params({
    # coefficient for L1 penalty
    'c1': 0.1,

    # coefficient for L2 penalty
    'c2': 0.01,

    # maximum number of iterations
    'max_iterations': 200,

    # whether to include transitions that
    # are possible, but not observed
    'feature.possible_transitions': True
})

# Provide a file name as a parameter to the train function, such that
# the model will be saved to the file when training is finished
trainer.train('ucla.model')



