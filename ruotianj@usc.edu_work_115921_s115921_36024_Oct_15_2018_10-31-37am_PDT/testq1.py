#!/usr/bin/env python
import distsim
word_to_ccdict = distsim.load_contexts("nytcounts.university_cat_dog")
print "Cosine similarity between cat and dog" ,distsim.cossim_sparse(word_to_ccdict['cat'],word_to_ccdict['dog'])
print "Cosine similarity between cat and university" ,distsim.cossim_sparse(word_to_ccdict['cat'],word_to_ccdict['university'])
print "Cosine similarity between university and dog" ,distsim.cossim_sparse(word_to_ccdict['university'],word_to_ccdict['dog'])
