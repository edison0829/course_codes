#!/bin/python
import os
def preprocess_corpus(train_sents):
    # counts
    ftrs = []
    files = os.listdir('data/lexicon')
    for j in train_sents:
        ftr = []
        se = ' '.join(j)
        for name in files:
            count = 0
            with open('data/lexicon/'+name) as f:
                lines = f.read().splitlines()
                for i in lines:
                    if i.decode('utf-8') in se:
                        count += 1
            f.close()
            ftr.append(count)
        ftrs.append(ftr)
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    return ftrs

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # 1. Use upper case to describe the word.
    ftrs.append("UCASE=" + word.upper())
    # 2. Number of characters
    ftrs.append("Len_Str=" + str(len(word)))
    # 5. word after strip
    ftrs.append("Num_char=" + word.strip('@#$%^&*'))


    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    # 3. The isalpha() methods return True if all
    # characters in the string are alphabets, Otherwise, It returns False.
    if word.isalpha():
        ftrs.append("IS_ALPHA")
    # 4. The method isdecimal() checks whether the string consists of only
    # decimal characters. This method are present only on unicode objects.
    if word.isdecimal():
        ftrs.append("IS_DECIMAL")




    # unuseful
    # 8. Existing '@' or not
    # if '@' in word:
    #     ftrs.append("@_EXIST")
    # # 6. The word is an URL of a website or not
    # if 'http:' in word:
    #     ftrs.append("IS_WEB")
    # # 7. Beginning word as a feature.
    # if word[0].isupper():
    #     ftrs.append("1_IS_UP")
    # else:
    #     ftrs.append("1_IS_LOW")

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
        [u'@SammieLynnsMom', u'@tg10781', u'they', u'will', u'be', u'all', u'done', u'by', u'Sunday', u'trust', u'me',
         u'*wink*']]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
