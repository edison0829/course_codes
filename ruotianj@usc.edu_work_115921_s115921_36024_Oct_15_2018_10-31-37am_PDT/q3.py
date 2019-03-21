#!/usr/bin/env python
import distsim

word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below


###Answer examples; replace with your choices
# a name (for example: person, organization, or location)
print 'china'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['china'],set(['china']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
# a common noun
print 'human'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['human'],set(['human']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
# an adjective
print 'handsome'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['handsome'],set(['handsome']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
# a verb
print 'fight'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['fight'],set(['fight']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
# another two words
print 'homes'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['homes'],set(['homes']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print 'cars'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['cars'],set(['cars']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))