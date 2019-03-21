#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples; replace with your choices
print 'china'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['china'],set(['china']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))
print 'human'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['human'],set(['human']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))
print 'handsome'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['handsome'],set(['handsome']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))
print 'fight'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['fight'],set(['fight']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))
print 'homes'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['homes'],set(['homes']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))
print 'cars'
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['cars'],set(['cars']),distsim.cossim_dense),start=1):
    print("{}: {} ({})".format(i, word, score))