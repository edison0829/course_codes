#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.university_cat_dog")
print "Cosine similarity between cat and dog" ,distsim.cossim_dense(word_to_vec_dict['cat'],word_to_vec_dict['dog'])
print "Cosine similarity between cat and university" ,distsim.cossim_dense(word_to_vec_dict['cat'],word_to_vec_dict['university'])
print "Cosine similarity between university and dog" ,distsim.cossim_dense(word_to_vec_dict['university'],word_to_vec_dict['dog'])

word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.university_cat_dog")
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['dog'], set(['dog']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
